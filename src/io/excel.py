from pathlib import Path
import pandas as pd
from pyspark.sql import functions as sf
from pyspark.sql import DataFrame, SparkSession
from src.extract.core.planning.plan_item import PlanItem
from src.models.excel import ExcelReadTask
import re


def excel_engine(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".xlsx":
        return "openpyxl"
    elif ".xls":
        return "xlrd"
    raise ValueError(f"Unsupported excel extension: {ext} ({path})")


def resolve_sheet_name(engine: str, path: str, requested: str) -> str:
    wb = pd.ExcelFile(path, engine=engine)
    sheets = wb.sheet_names

    # Exact or case insenstive
    if requested in sheets:
        return requested
    for s in sheets:
        if s.lower() == requested.lower():
            return s

    # TJ special case
    if requested.lower() == "tj":
        for s in sheets:
            if s.casefold().startswith("tj"):
                return s

    raise ValueError(f"Could not resolve {requested} sheet name.")


def build_excel_read_plan(cfg: dict) -> list[ExcelReadTask] | None:
    tasks = []

    try:
        cfg["sheets"]

    except TypeError:
        return None

    for sheet in cfg["sheets"]:
        selected_ids = [selected_id for selected_id in sheet["select"]]
        requested_sections = [
            section for section in sheet["sections"] if section["id"] in selected_ids
        ]
        sheet_tasks = [
            ExcelReadTask(
                sheet=sheet["name"],
                section=section["id"],
                header_row=section["header_row"],
                row_start=section["row_range"]["start"],
                row_end=section["row_range"]["end"],
            )
            for section in requested_sections
        ]
        tasks.extend(sheet_tasks)

    return tasks


def read_excel_to_pd(path: str, task: ExcelReadTask):
    engine = excel_engine(path)
    resolved_sheet_name = resolve_sheet_name(engine, path, task.sheet)
    header_pd_index = task.header_row - 1

    df = pd.read_excel(
        path,
        sheet_name=resolved_sheet_name,
        header=header_pd_index,
    )

    df = df.iloc[task.row_start : (task.row_end + 1), 1::]

    return resolved_sheet_name, df


def read_excel_to_spark(
    spark_session: SparkSession,
    paths,
    tasks: list[ExcelReadTask],
    mode: str,
) -> list[dict[str, DataFrame]]:
    match mode:
        case "single":
            files_list = []
            for path in paths:
                if len(tasks) != 1:
                    raise ValueError(
                        f"Single mode expects exactly 1 ExcelReadTask, got {len(tasks)}"
                    )
                for task in tasks:
                    _, df = read_excel_to_pd(path, task)

                    df = df.astype(str)

                    df_sp = spark_session.createDataFrame(df)

                    files_list.append(df_sp)

            return files_list

        case "dict":
            files_list = []
            for path in paths:
                d = {}
                for task in tasks:
                    resolved_sheet_name, df = read_excel_to_pd(path, task)
                    key = f"{(task.sheet).upper()}::{(task.section).upper()}"

                    # If path includes a number we might add it as _year
                    pattern = r"\d{4}"

                    match = re.search(pattern, str(path))

                    if match:
                        df["_year"] = match.group(0)

                    # add the sheet name
                    df["_sheet_name"] = resolved_sheet_name

                    # add the _source_fi
                    df["_source_fi"] = Path(path).name

                    df = df.astype(str)
                    d[key] = spark_session.createDataFrame(df)

                files_list.append(d)
            return files_list
