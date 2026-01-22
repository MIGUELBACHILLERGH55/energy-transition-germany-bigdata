from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as sf
from src.gold.io.paths import resolve_gold_dataset_path
from src.io.path_resolver import resolve_output_path
from src.config.loader import config
from pathlib import Path


class RenewablesByTechnology:
    def __init__(self, spark_session: SparkSession):
        self.spark_session = spark_session

    @property
    def input_path(self):
        proj_config = config.project_config
        ageb_source = config.sources["ageb"]

        for _, dataset_cfg in ageb_source.datasets.items():
            return resolve_output_path(proj_config, dataset_cfg, "silver")

    def read_inputs(self) -> DataFrame:
        input_path = self.input_path.as_posix()
        df = self.spark_session.read.parquet(input_path)
        df = df.filter("table_id IN (3.1)")
        return df

    def transform(self, df: DataFrame) -> DataFrame:
        df = df.withColumn("dataset", sf.lit("renewables_by_technology"))

        df = df.withColumnRenamed("dimension", "technology")

        renewables_by_technology_cols = (
            "year",
            "technology",
            "value",
            "unit",
            "dataset",
        )

        df = df.select(*renewables_by_technology_cols)

        return df

    def write(self, df: DataFrame):
        output_path: Path = resolve_gold_dataset_path("renewables_by_technology")
        (
            df.coalesce(1)
            .write.mode("overwrite")
            .option("header", "true")
            .option("delimiter", ",")
            .csv(output_path.as_posix())
        )

        # Find the part file and rename it
        part_file = next(output_path.glob("part*.csv"))

        final_file = output_path / "renewables_by_technology.csv"
        part_file.rename(final_file)

        # Delete _SUCCESS
        success = output_path / "_SUCCESS"
        if success.exists():
            success.unlink()

    def run(self):
        df = self.read_inputs()
        df = self.transform(df)
        self.write(df)
