# Smard Pipeline inherits from batch_transformer
from pyspark.sql import DataFrame, Row
from src.transform.core.pipelines.batch_transformer import BatchTransformerPipeline
import json
from datetime import date


from pathlib import Path
from src.io.path_resolver import resolve_output_path


class SmardTimeseriesPipeline(BatchTransformerPipeline):
    def read_bronze_paths(self) -> dict[str, list[Path | str]]:
        bronze_paths: dict[str, list[Path | str]] = {}

        for ds_name, ds in self.source.datasets.items():
            if not ds.enabled:
                continue
            bronze_paths[ds_name] = [
                resolve_output_path(self.project_config, ds, layer="bronze")
            ]

        return bronze_paths

    def read_bronze(self, bronze_path: Path) -> DataFrame:
        rows = []

        for file in bronze_path.iterdir():
            payload = json.load(open(file))
            meta = payload["meta"]

            for item in payload["data"]:
                ts_ms = item["timestamps_ms"]
                value = item["value"]
                if value is None:
                    continue

                data_date = date.fromisoformat(meta["data_date"])
                run_date = date.fromisoformat(meta["run_date"])

                rows.append(
                    Row(
                        timestamp=ts_ms,
                        value=value,
                        dataset_name=meta["dataset"],
                        filter_id=meta["filter_id"],
                        resolution=meta["resolution"],
                        data_date=data_date,
                        run_date=run_date,
                    )
                )

        return self.spark.createDataFrame(rows)

    def apply_steps(self, ds_name: str, df: DataFrame, verbose=False) -> DataFrame:
        return df

    def write_silver(self, ds_name: str, df: DataFrame) -> None:
        ds = self.source.datasets[ds_name]
        silver_path = resolve_output_path(self.project_config, ds, layer="silver")
        (df.write.mode("append").partitionBy("data_date").parquet(str(silver_path)))

    def run(self) -> None:
        bronze_paths = self.read_bronze_paths()

        for ds_name, bronze_paths in bronze_paths.items():
            for path in bronze_paths:
                df = self.read_bronze(path)
                df2 = self.apply_steps(ds_name, df)
                self.write_silver(ds_name, df2)
