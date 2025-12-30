from pathlib import Path
import pandas as pd
from pyspark.sql import functions as sf
from pyspark.sql import DataFrame, SparkSession
from src.extract.core.planning.plan_item import PlanItem
from src.models.excel import ExcelReadTask


def excel_engine(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".xlsx":
        return "openpyxl"
    elif ".xls":
        return "xlrd"
    raise ValueError(f"Unsupported excel extension: {ext} ({path})")


def resolve_sheet_name(engine: str, path: Path, requested: str) -> str:
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


def build_excel_read_plan(cfg: dict):
    tasks = []
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


def read_excel_to_spark(
    spark_session: SparkSession,
    paths,
    tasks: list[ExcelReadTask],
    mode: str = "dict",
    union_by_name: bool = True,
):
    print("Trouble shooting message")
    for path in paths:
        for task in tasks:
            engine = excel_engine(path)
            resolved_sheet_name = resolve_sheet_name(engine, path, task.sheet)

            df = pd.read_excel(
                path,
                sheet_name=resolved_sheet_name,
                header=task.header_row,
            )
            df.head()

            # Primero leer todo luego cortar

    match mode:
        case "single":
            pass
        case "dict":
            pass
        case "union":
            pass
