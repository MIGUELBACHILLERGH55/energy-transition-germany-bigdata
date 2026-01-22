from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as sf
from pathlib import Path

from src.config.loader import config
from src.io.path_resolver import resolve_output_path
from src.gold.io.paths import resolve_gold_dataset_path


class ElectricityPriceTrendsMonthly:
    """
    BI-ready monthly electricity price trends.

    - SMARD market prices aggregated to monthly average (EUR/MWh)
    - Eurostat HICP Energy index (monthly, index 2015=100)
    - One row per month and price_type
    """

    def __init__(self, spark_session: SparkSession):
        self.spark = spark_session
        self.proj_config = config.project_config
        self.smard_source = config.sources["smard"]
        self.eurostat_source = config.sources["eurostat"]

    # ---------- READ ----------

    def read_smard_prices(self) -> DataFrame:
        dataset_cfg = self.smard_source.datasets["prices"]
        path = resolve_output_path(self.proj_config, dataset_cfg, "silver")
        df = self.spark.read.parquet(path.as_posix())

        return df

    def read_eurostat_prices(self) -> DataFrame:
        dataset_cfg = self.eurostat_source.datasets["hicp_energy_index"]
        path = resolve_output_path(self.proj_config, dataset_cfg, "silver")
        df = self.spark.read.parquet(path.as_posix())

        return df

    # ---------- TRANSFORM ----------

    def transform_smard_monthly(self, df: DataFrame) -> DataFrame:
        df_monthly = (
            df.withColumn("date", sf.trunc(sf.to_date("timestamp"), "month"))
            .groupBy("date")
            .agg(sf.avg("value").alias("price_value"))
            .withColumn("year", sf.year("date"))
            .withColumn("price_type", sf.lit("market_price"))
            .withColumn("unit", sf.lit("EUR/MWh"))
            .withColumn("source", sf.lit("SMARD"))
            .withColumn("resolution", sf.lit("month"))
            .select(
                "date",
                "year",
                "price_value",
                "price_type",
                "unit",
                "source",
                "resolution",
            )
            .orderBy("date")
        )

        return df_monthly

    def transform_eurostat_monthly(self, df: DataFrame) -> DataFrame:
        df_monthly = (
            df.withColumn("date", sf.trunc("date", "month"))
            .withColumnRenamed("value", "price_value")
            .withColumn("year", sf.year("date"))
            .withColumn("price_type", sf.lit("consumer_price_index"))
            .withColumn("unit", sf.lit("index (2015=100)"))
            .withColumn("source", sf.lit("Eurostat"))
            .withColumn("resolution", sf.lit("month"))
            .select(
                "date",
                "year",
                "price_value",
                "price_type",
                "unit",
                "source",
                "resolution",
            )
            .orderBy("date")
        )

        return df_monthly

    def transform(self, df_smard: DataFrame, df_eurostat: DataFrame) -> DataFrame:
        df_market = self.transform_smard_monthly(df_smard)
        df_hicp = self.transform_eurostat_monthly(df_eurostat)

        df_final = df_market.unionByName(df_hicp)

        return df_final

    # ---------- WRITE ----------

    def write(self, df: DataFrame):
        output_path: Path = resolve_gold_dataset_path(
            "electricity_price_trends_monthly"
        )

        (
            df.coalesce(1)
            .write.mode("overwrite")
            .option("header", "true")
            .csv(output_path.as_posix())
        )

        # Rename part file to a friendly name
        part_file = next(output_path.glob("part-*.csv"))
        final_file = output_path / "electricity_price_trends_monthly.csv"
        part_file.rename(final_file)

        # Remove _SUCCESS file
        success_file = output_path / "_SUCCESS"
        if success_file.exists():
            success_file.unlink()

    # ---------- RUN ----------

    def run(self):
        df_smard = self.read_smard_prices()
        df_eurostat = self.read_eurostat_prices()

        df_gold = self.transform(df_smard, df_eurostat)
        self.write(df_gold)
