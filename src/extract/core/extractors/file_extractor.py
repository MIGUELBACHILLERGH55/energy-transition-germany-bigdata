from pathlib import Path
from pyspark.sql.types import StructType
from pyspark.sql import SparkSession, DataFrame
from src.config.models.project_models import ProjectConfig
from src.config.models.source_models import SourceSpec
from src.extract.core.planning import plan_item
from src.io.path_resolver import resolve_input_path, resolve_output_path
from src.extract.core.planning.plan_item import PlanItem
from src.config.loader import config
import pandas as pd


class FileExtractor:
    def __init__(
        self,
        project_config: ProjectConfig,
        source: SourceSpec,
        spark_session: SparkSession,
        dataset_name: str | None = None,
        mode: str = "overwrite",
    ):
        self.project_config = project_config
        self.source = source
        self.spark_session = spark_session
        self.dataset_name = dataset_name
        self.mode = mode

    def plan(self) -> list[PlanItem]:
        if self.dataset_name:
            pass
        l = []
        for dataset_name, dataset_cfg in self.source.datasets.items():
            if dataset_cfg.enabled:
                pi = PlanItem(
                    source_name=self.source.name,
                    dataset_name=dataset_name,
                    dataset_id=dataset_cfg.metadata.dataset_id,
                    input_path=resolve_input_path(self.project_config, dataset_cfg),
                    input_format=dataset_cfg.storage["format"],
                    output_path=resolve_output_path(
                        self.project_config, dataset_cfg, "bronze"
                    ),
                )
                l.append(pi)
        return l

    def read_files(self, pi: PlanItem) -> list[Path]:
        path = pi.input_path

        if path.is_dir():
            return list(path.glob("*"))
        elif "*" in str(path):
            return list(path.parent.glob(path.name))
        else:
            return [path]

    def transform(self, pi: PlanItem, files: list[Path]) -> DataFrame:
        paths = [str(f) for f in files]

        match pi.input_format:
            # ----------------------------
            # CSV
            # ----------------------------
            case "csv":
                return (
                    self.spark_session.read.option("header", True)
                    .option("inferSchema", True)
                    .csv(paths)
                )

            # ----------------------------
            # JSON
            # ----------------------------
            case "json":
                return self.spark_session.read.option("multiLine", True).json(
                    paths
                )  # útil para JSONs “bonitos”

            # ----------------------------
            # EXCEL (requiere spark-excel)
            # ----------------------------
            case "excel" | "xlsx" | "xls":
                return (
                    self.spark_session.read.format("com.crealytics.spark.excel")
                    .option("header", True)
                    .option("inferSchema", True)
                    .option("dataAddress", "'Sheet1'!")  # sheet por defecto
                    .load(paths)
                )

            # ----------------------------
            # ERROR
            # ----------------------------
            case _:
                raise ValueError(
                    f"Unsupported input_format '{pi.input_format}' "
                    f"for dataset {pi.dataset_id}"
                )

    def persist_bronze(self, pi: PlanItem, df: DataFrame) -> None:
        """
        Writes the ingested dataset to the bronze layer.
        Expects pi.output_path to be a directory (not a file).
        """
        output = str(pi.output_path)

        writer = df.write.mode(self.mode)

        partition_cols = getattr(pi, "partition_cols", None)
        if partition_cols:
            writer = writer.partitionBy(*partition_cols)

        # Bronze as parquet (recommended for file ingestion)
        writer.parquet(output)

    def run(self):
        items = self.plan()
        for pi in items:
            files = self.read_files(pi)
            df = self.transform(pi, files)
            self.persist_bronze(pi, df)
