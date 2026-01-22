from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as sf
from src.gold.io.paths import resolve_gold_dataset_path
from src.io.path_resolver import resolve_output_path
from src.config.loader import config
from pathlib import Path


class DailyElectricityProfile:
    def __init__(self, spark_session: SparkSession):
        self.spark_session = spark_session

    @property
    def input_path(self):
        proj_config = config.project_config
        opsd_source = config.sources["opsd"]

        for _, dataset_cfg in opsd_source.datasets.items():
            return resolve_output_path(proj_config, dataset_cfg, "silver")

    def read_inputs(self) -> DataFrame:
        input_path = self.input_path.as_posix()
        df = self.spark_session.read.parquet(input_path)
        return df

    def transform(self, df: DataFrame) -> DataFrame:
        df = df.withColumnRenamed("event_date_utc", "date")

        df = df.groupBy("date").agg(
            sf.sum("load_act").alias("load_act_daily"),
            sf.sum(sf.coalesce(sf.col("solar_gen"), sf.lit(0))).alias(
                "solar_gen_daily"
            ),
            sf.sum(sf.coalesce(sf.col("wind_gen"), sf.lit(0))).alias("wind_gen_daily"),
        )

        df = df.withColumn(
            "renewables_gen_daily",
            sf.col("wind_gen_daily") + sf.col("solar_gen_daily"),
        )

        df = (
            df.withColumn(
                "renewables_share",
                sf.col("renewables_gen_daily") / sf.col("load_act_daily"),
            )
            .withColumn(
                "solar_share",
                sf.col("solar_gen_daily") / sf.col("load_act_daily"),
            )
            .withColumn(
                "wind_share",
                sf.col("wind_gen_daily") / sf.col("load_act_daily"),
            )
        )

        df = (
            df.withColumn("year", sf.year("date"))
            .withColumn("month", sf.month("date"))
            .withColumn("month_name", sf.date_format("date", "MMMM"))
            .withColumn("day_of_week", sf.date_format("date", "E"))
            .withColumn("is_weekend", sf.dayofweek("date").isin([1, 7]))
        )

        df = df.dropna(subset="load_act_daily")

        df = df.withColumn("dataset", sf.lit("daily_electricity_profile"))

        daily_cols = (
            "date",
            "year",
            "month",
            "month_name",
            "day_of_week",
            "is_weekend",
            "load_act_daily",
            "solar_gen_daily",
            "wind_gen_daily",
            "renewables_gen_daily",
            "renewables_share",
            "solar_share",
            "wind_share",
            "dataset",
        )

        df = df.select(*daily_cols)

        df = df.sort("date")

        df.show()

        return df

    def write(self, df: DataFrame):
        output_path: Path = resolve_gold_dataset_path("daily_electricity_profile")
        (
            df.coalesce(1)
            .write.mode("overwrite")
            .option("header", "true")
            .option("delimiter", ",")
            .csv(output_path.as_posix())
        )

        # Find the part file and rename it
        part_file = next(output_path.glob("part*.csv"))

        final_file = output_path / "daily_electricity_profile.csv"
        part_file.rename(final_file)

        # Delete _SUCCESS
        success = output_path / "_SUCCESS"
        if success.exists():
            success.unlink()

    def run(self):
        df = self.read_inputs()
        df = self.transform(df)
        self.write(df)
