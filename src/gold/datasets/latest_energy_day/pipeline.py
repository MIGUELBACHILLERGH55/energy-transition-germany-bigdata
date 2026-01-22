from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as sf
from src.gold.io.paths import resolve_gold_dataset_path
from src.io.path_resolver import resolve_output_path
from src.config.loader import config
from pathlib import Path


class LatestEnergyDay:
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
        # --------------------------------------------------
        # STEP 0: Keep only hourly data
        # --------------------------------------------------
        df = df.filter(sf.col("resolution") == sf.lit("hour"))

        # --------------------------------------------------
        # STEP 1: Find latest FULL day using LOAD
        # --------------------------------------------------
        load_df = df.filter(sf.col("dataset_name") == sf.lit("load"))

        full_days = (
            load_df.groupBy(sf.to_date("timestamp").alias("day"))
            .agg(sf.countDistinct("timestamp").alias("n_hours"))
            .filter(sf.col("n_hours") == 24)
        )

        latest_day = full_days.select(sf.max("day").alias("latest_day")).collect()[0][
            "latest_day"
        ]

        # --------------------------------------------------
        # STEP 2: Filter to latest full day
        # --------------------------------------------------
        df = df.filter(sf.to_date("timestamp") == sf.lit(latest_day))

        # --------------------------------------------------
        # STEP 3: Keep only load & price
        # --------------------------------------------------
        df = df.filter(sf.col("dataset_name").isin(["load", "prices"]))

        # --------------------------------------------------
        # STEP 4: Derive metric
        # --------------------------------------------------
        df = df.withColumn(
            "metric",
            sf.when(sf.col("dataset_name") == "load", sf.lit("load")).when(
                sf.col("dataset_name") == "prices", sf.lit("price")
            ),
        )

        # --------------------------------------------------
        # STEP 5: Derive unit
        # --------------------------------------------------
        df = df.withColumn(
            "unit",
            sf.when(sf.col("metric") == "load", sf.lit("MW")).when(
                sf.col("metric") == "price", sf.lit("EUR/MWh")
            ),
        )

        # --------------------------------------------------
        # STEP 6: Tag dataset
        # --------------------------------------------------
        df = df.withColumn("dataset", sf.lit("latest_energy_day"))

        # --------------------------------------------------
        # STEP 7: Drop junk columns
        # --------------------------------------------------
        df = df.drop(
            "filter_id",
            "resolution",
            "dataset_name",
            "event_date",
        )

        df.filter(sf.col("metric") == "price").show()

        return df

    def write(self, df: DataFrame):
        output_path: Path = resolve_gold_dataset_path("latest_energy_day")
        (
            df.coalesce(1)
            .write.mode("overwrite")
            .option("header", "true")
            .option("delimiter", ",")
            .csv(output_path.as_posix())
        )

        # Find the part file and rename it
        part_file = next(output_path.glob("part*.csv"))

        final_file = output_path / "latest_energy_day.csv"
        part_file.rename(final_file)

        # Delete _SUCCESS
        success = output_path / "_SUCCESS"
        if success.exists():
            success.unlink()

    def run(self):
        df = self.read_inputs()
        df = self.transform(df)
        self.write(df)
