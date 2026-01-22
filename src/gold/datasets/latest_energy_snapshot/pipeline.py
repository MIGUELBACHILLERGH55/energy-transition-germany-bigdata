from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as sf
from src.gold.io.paths import resolve_gold_dataset_path
from src.io.path_resolver import resolve_output_path
from src.config.loader import config
from pathlib import Path


class LatestEnergySnapshot:
    def __init__(self, spark_session: SparkSession):
        self.spark_session = spark_session

    @property
    def input_paths(self):
        proj_config = config.project_config
        smard_source = config.sources["smard"]

        paths = []
        for _, dataset_cfg in smard_source.datasets.items():
            paths.append(resolve_output_path(proj_config, dataset_cfg, "silver"))

        return paths

    def read_inputs(self) -> DataFrame:
        input_paths = [path.as_posix() for path in self.input_paths]
        df_prices = self.spark_session.read.parquet(input_paths[0])
        df_generation = self.spark_session.read.parquet(input_paths[1])

        # Have to change this so it filters
        return df_generation.unionByName(df_prices)

    def transform(self, df: DataFrame) -> DataFrame:
        df = df.withColumn("dataset", sf.lit("latest_energy_snapshot"))

        df = df.withColumnRenamed("dataset_name", "metric")

        df = df.withColumn(
            "metric_type",
            sf.when(sf.col("metric") == "prices", sf.lit("price")).otherwise(
                sf.lit("generation")
            ),
        )

        df = df.withColumn(
            "unit",
            sf.when(sf.col("metric_type").isin("price"), sf.lit("EUR/MWh")).otherwise(
                sf.lit("MW")
            ),
        )

        df = df.withColumn(
            "timestamp",
            sf.to_timestamp(sf.from_unixtime(sf.col("timestamp") / 1000)),
        )

        latest_energy_snapshot_cols = (
            "timestamp",
            "metric",
            "metric_type",
            "value",
            "unit",
            "run_date",
            "dataset",
        )
        df = df.select(*latest_energy_snapshot_cols)

        df.show()

        return df

    def write(self, df: DataFrame):
        output_path: Path = resolve_gold_dataset_path("latest_energy_snapshot")
        (
            df.coalesce(1)
            .write.mode("overwrite")
            .option("header", "true")
            .option("delimiter", ",")
            .csv(output_path.as_posix())
        )

        # Find the part file and rename it
        part_file = next(output_path.glob("part*.csv"))

        final_file = output_path / "latest_energy_snapshot.csv"
        part_file.rename(final_file)

        # Delete _SUCCESS
        success = output_path / "_SUCCESS"
        if success.exists():
            success.unlink()

    def run(self):
        df = self.read_inputs()
        df = self.transform(df)
        # self.write(df)
