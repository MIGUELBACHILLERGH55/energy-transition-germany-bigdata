from pathlib import Path
from pyspark.sql import SparkSession, DataFrame
from src.config.models.project_models import ProjectConfig
from src.config.models.source_models import SourceSpec
from src.io.path_resolver import resolve_input_path, resolve_output_path
from src.extract.core.planning.plan_item import PlanItem
from src.io.excel import build_excel_read_plan, read_excel_to_spark


class FileExtractor:
    def __init__(
        self,
        project_config: ProjectConfig,
        source: SourceSpec,
        spark_session: SparkSession,
        dataset_name: str | None = None,
        mode: str = "append",
    ):
        self.project_config = project_config
        self.source = source
        self.spark_session = spark_session
        self.dataset_name = dataset_name
        self.mode = mode

    def plan(self) -> list[PlanItem]:
        if self.dataset_name:
            pass
        plan_item_list = []
        for dataset_name, dataset_cfg in self.source.datasets.items():
            if dataset_cfg.enabled:
                # Rewrite this so plan item includes read options, each DatasetSpec may also contain the excel config
                # that would helpt to read all the xlsx
                pi = PlanItem(
                    source_name=self.source.name,
                    dataset_name=dataset_name,
                    dataset_id=dataset_cfg.metadata.dataset_id,
                    input_path=resolve_input_path(self.project_config, dataset_cfg),
                    input_format=dataset_cfg.storage["format"],
                    output_path=resolve_output_path(
                        self.project_config,
                        dataset_cfg,
                        "bronze",
                    ),
                    # Resolve and build here the list of ExcelReadTask
                    excel_tasks=build_excel_read_plan(dataset_cfg.excel),
                    partitioning=dataset_cfg.destinations["bronze"].partitioning,
                )
                plan_item_list.append(pi)
        return plan_item_list

    def read_files(self, pi: PlanItem) -> list[Path]:
        path = Path(pi.input_path)

        if "*" in str(path):
            files = sorted(path.parent.glob(path.name))
            if not files:
                raise FileNotFoundError(f"Pattern matched 0 files: {path}")
            return files

        # 2) If it's a directory, return all files inside
        if path.is_dir():
            files = sorted([p for p in path.iterdir() if p.is_file()])
            if not files:
                raise FileNotFoundError(f"Directory has 0 files: {path}")
            return files

        # 3) If it's a single file, return it
        if path.is_file():
            return [path]

        # 4) Nothing matched → clear error
        raise FileNotFoundError(f"Input path not found: {path}")

    def transform(self, pi: PlanItem, files: list[Path]) -> list[dict[str, DataFrame]]:
        paths = [str(f) for f in files]

        match pi.input_format:
            # ----------------------------
            # CSV
            # ----------------------------
            case "csv":
                return [
                    {
                        "main": (
                            self.spark_session.read.option("header", True)
                            .option("inferSchema", True)
                            .csv(paths)
                        )
                    }
                ]

            # ----------------------------
            # JSON
            # ----------------------------
            case "json":
                return [
                    {
                        "main": self.spark_session.read.option("multiLine", True).json(
                            paths
                        )
                    }
                ]

            # ----------------------------
            # EXCEL (requiere spark-excel)
            # ----------------------------
            case "excel" | "xlsx" | "xls":
                # Here we will use a dedicated function that would use excel_plan to resolve which sheets to select
                return read_excel_to_spark(
                    spark_session=self.spark_session,
                    paths=paths,
                    tasks=pi.excel_tasks,
                    mode="dict",
                )

            # ----------------------------
            # ERROR
            # ----------------------------
            case _:
                raise ValueError(
                    f"Unsupported input_format '{pi.input_format}' "
                    f"for dataset {pi.dataset_id}"
                )

    def persist_bronze(self, pi: PlanItem, df: DataFrame, folder=None) -> None:
        """
        Writes the ingested dataset to the bronze layer.
        Expects pi.output_path to be a directory (not a file).
        """
        if not folder:
            output = str(pi.output_path)
        else:
            output = str(pi.output_path / folder)

        writer = df.write.mode(self.mode)

        partition_cols = getattr(pi, "partitioning", None)
        if partition_cols:
            writer = writer.partitionBy(*partition_cols)

        # Bronze as parquet (recommended for file ingestion)
        writer.parquet(output)

    def run(self):
        items = self.plan()
        for pi in items:
            files = self.read_files(pi)
            list_dicts = self.transform(pi, files)
            for dict_ in list_dicts:
                for key, df in dict_.items():
                    if key == "main":
                        self.persist_bronze(pi, df)
                    else:
                        key_sanitized = key.replace("::", "__")
                        self.persist_bronze(pi, df, key_sanitized)
