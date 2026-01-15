from src.io.path_resolver import resolve_output_path
from pyspark.sql import SparkSession, DataFrame
from pathlib import Path

# Generic pipelines, reads bronze -> applies steps
# and writes silver


class BatchTransformerPipeline:
    def __init__(self, spark: SparkSession, project_config, source):
        self.spark = spark
        self.project_config = project_config
        self.source = source

    def read_bronze_paths(self) -> dict[str, list[Path | str]]:
        bronze_paths: dict[str, list[Path | str]] = {}

        # Rewrite this contract so it returns list of paths

        for ds_name, ds in self.source.datasets.items():
            if not ds.enabled:
                continue
            bronze_paths[ds_name] = [
                resolve_output_path(self.project_config, ds, layer="bronze")
            ]

        return bronze_paths

    def read_bronze(self, bronze_path: Path) -> DataFrame:
        return self.spark.read.parquet(str(bronze_path))

    def apply_steps(self, ds_name: str, df: DataFrame) -> DataFrame:
        # de momento “passthrough” o 2-3 cosas básicas
        # (renames, casts, timestamp parsing, drop nulls…)
        return df

    def write_silver(self, ds_name: str, df: DataFrame) -> None:
        ds = self.source.datasets[ds_name]
        silver_path = resolve_output_path(self.project_config, ds, layer="silver")
        (df.write.mode("append").parquet(str(silver_path)))

    def run(self) -> None:
        bronze_paths = self.read_bronze_paths()

        for ds_name, bronze_paths in bronze_paths.items():
            for path in bronze_paths:
                df = self.read_bronze(path)
                df2 = self.apply_steps(ds_name, df)
                self.write_silver(ds_name, df2)
