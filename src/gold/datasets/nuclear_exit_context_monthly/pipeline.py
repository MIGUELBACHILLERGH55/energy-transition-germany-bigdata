from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as sf
from pathlib import Path

from src.config.loader import config
from src.io.path_resolver import resolve_output_path
from src.gold.io.paths import resolve_gold_dataset_path


class NuclearExitContextMonthly:
    """
    Contextual dataset describing the phase-out of nuclear energy in Germany.

    - Based on SMARD nuclear electricity generation data
    - Monthly aggregation
    - BI-ready for before/after nuclear exit analysis
    """

    def __init__(self, spark_session: SparkSession):
        self.spark = spark_session
        self.proj_config = config.project_config
        self.smard_source = config.sources["smard"]

    # ---------- READ ----------

    def read_nuclear_generation(self) -> DataFrame:
        dataset_cfg = self.smard_source.datasets["nuclear_energy"]
        path = resolve_output_path(self.proj_config, dataset_cfg, "silver")
        nuclear_path = path / "dataset_name=nuclear_energy"
        df = self.spark.read.parquet(nuclear_path.as_posix())
        return df

    # ---------- TRANSFORM ----------
    def transform_monthly(self, df: DataFrame) -> DataFrame:
        """
        Build a monthly nuclear generation time series.

        Input:
        - SMARD nuclear_energy dataset (daily resolution)

        Output:
        - One row per month with total nuclear electricity generation
        """

        df_monthly = (
            df
            # Keep only daily data
            .filter(sf.col("resolution") == "day")
            # Truncate timestamp to month
            .withColumn("date", sf.trunc(sf.to_date("timestamp"), "month"))
            # Explicit technology label (dataset is nuclear-only)
            .withColumn("technology", sf.lit("nuclear"))
            # Monthly aggregation
            .groupBy("date", "technology")
            .agg(sf.sum("value").alias("generation_value"))
            # Temporal dimension
            .withColumn("year", sf.year("date"))
            # Explicit unit (not present in source)
            .withColumn("unit", sf.lit("MWh"))
            # Pre / post nuclear exit labeling
            .withColumn(
                "period",
                sf.when(sf.col("date") < sf.lit("2023-04-01"), "pre_exit").otherwise(
                    "post_exit"
                ),
            )
            # Dataset identifier
            .withColumn("dataset", sf.lit("nuclear_exit_context_monthly"))
            # Final column selection
            .select(
                "date",
                "year",
                "technology",
                "generation_value",
                "unit",
                "period",
                "dataset",
            )
            # Ordered output for BI tools
            .orderBy("date")
        )

        return df_monthly

    # ---------- WRITE ----------

    def write(self, df: DataFrame):
        output_path: Path = resolve_gold_dataset_path("nuclear_exit_context_monthly")

        (
            df.coalesce(1)
            .write.mode("overwrite")
            .option("header", "true")
            .csv(output_path.as_posix())
        )

        part_file = next(output_path.glob("part-*.csv"))
        final_file = output_path / "nuclear_exit_context_monthly.csv"
        part_file.rename(final_file)

        success = output_path / "_SUCCESS"
        if success.exists():
            success.unlink()

    # ---------- RUN ----------

    def run(self):
        df_nuclear = self.read_nuclear_generation()
        df_gold = self.transform_monthly(df_nuclear)
        self.write(df_gold)
