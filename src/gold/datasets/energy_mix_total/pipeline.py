from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as sf
from src.gold.io.paths import resolve_gold_dataset_path
from src.io.path_resolver import resolve_output_path
from src.config.loader import config
from pathlib import Path


class EnergyMixTotal:
    def __init__(self, spark_session: SparkSession):
        self.spark_session = spark_session

    @property
    def input_path(self):
        proj_config = config.project_config
        ageb_source = config.sources["ageb"]

        for _, dataset_cfg in ageb_source.datasets.items():
            return resolve_output_path(proj_config, dataset_cfg, "silver")

    def read_inputs(self) -> DataFrame:
        return self.spark_session.read.parquet(f"{self.input_path}/table_id=6.1")

    def transform(self, df: DataFrame) -> DataFrame:
        # Ensure year is numeric
        df = df.withColumn("year", sf.col("year").cast("int"))
        # Add dataset name column for trazability
        df = df.withColumn("dataset", sf.lit("energy_mix_total"))

        # Percentage over year total, share
        df_total_year = df.groupBy("year").agg(sf.sum("value").alias("total_per_year"))

        df_final = df.join(df_total_year, on="year", how="left").withColumn(
            "share", sf.col("value") / sf.col("total_per_year")
        )
        df_final = df_final.drop("total_per_year")

        df_energy = (
            df_final.select("year", "dimension", "value", "dataset")
            .withColumn("metric", sf.lit("energy"))
            .withColumn("unit", sf.lit("PJ"))
        )

        df_share = (
            df_final.select("year", "dimension", "share", "dataset")
            .withColumnRenamed("share", "value")
            .withColumn("metric", sf.lit("share"))
            .withColumn("unit", sf.lit("ratio"))
        )

        df_long = (
            df_energy.unionByName(df_share)
            .select("year", "dimension", "metric", "value", "unit", "dataset")
            .orderBy("year", "dimension", "metric")
        )

        return df_long

    def write(self, df: DataFrame):
        output_path: Path = resolve_gold_dataset_path("energy_mix_total")
        (
            df.coalesce(1)
            .write.mode("overwrite")
            .option("header", "true")
            .option("delimiter", ",")
            .csv(output_path.as_posix())
        )

        # Find the part file and rename it
        part_file = next(output_path.glob("part*.csv"))

        final_file = output_path / "energy_mix_total.csv"
        part_file.rename(final_file)

        # Delete _SUCCESS
        success = output_path / "_SUCCESS"
        if success.exists():
            success.unlink()

    def run(self):
        df = self.read_inputs()
        df = self.transform(df)
        self.write(df)
