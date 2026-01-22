from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as sf
from pyspark.sql.window import Window
from src.gold.io.paths import resolve_gold_dataset_path
from src.io.path_resolver import resolve_output_path
from src.config.loader import config
from src.gold.datasets.final_energy_consumption_by_sector.mappings import (
    SECTOR_MAP,
)
from pathlib import Path


class FinalEnergyConsumptionBySector:
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
        df = df.filter("table_id IN (6.1, 6.2, 6.3, 6.4, 6.6)")
        return df

    def transform(self, df: DataFrame) -> DataFrame:
        # --------------------------------------------------
        # STEP 0: Dataset tag
        # --------------------------------------------------
        df = df.withColumn("dataset", sf.lit("final_energy_consumption_by_sector"))

        # --------------------------------------------------
        # STEP 1: Derive sector & rename dimension
        # --------------------------------------------------
        df = df.withColumn(
            "sector",
            sf.create_map([sf.lit(x) for x in sum(SECTOR_MAP.items(), ())])[
                sf.col("table_id")
            ],
        )

        df = df.withColumnRenamed("dimension", "energy_source")

        # --------------------------------------------------
        # STEP 2: Energy metric (absolute values)
        # --------------------------------------------------
        df_energy = df.select(
            "year",
            "sector",
            "energy_source",
            sf.lit("energy").alias("metric"),
            sf.col("value"),
            sf.col("unit"),
        )

        # --------------------------------------------------
        # STEP 3: Share metric (within sector & year)
        # --------------------------------------------------
        w_sector_year = Window.partitionBy("year", "sector")

        df_share = df.withColumn(
            "value", sf.col("value") / sf.sum("value").over(w_sector_year)
        ).select(
            "year",
            "sector",
            "energy_source",
            sf.lit("share").alias("metric"),
            "value",
            sf.lit("ratio").alias("unit"),
        )

        # --------------------------------------------------
        # STEP 4: Union + final polish
        # --------------------------------------------------
        df_final = (
            df_energy.unionByName(df_share)
            .withColumn("dataset", sf.lit("final_energy_consumption_by_sector"))
            .orderBy("year", "sector", "energy_source", "metric")
        )

        return df_final

    def write(self, df: DataFrame):
        output_path: Path = resolve_gold_dataset_path(
            "final_energy_consumption_by_sector"
        )
        (
            df.coalesce(1)
            .write.mode("overwrite")
            .option("header", "true")
            .option("delimiter", ",")
            .csv(output_path.as_posix())
        )

        # Find the part file and rename it
        part_file = next(output_path.glob("part*.csv"))

        final_file = output_path / "final_energy_consumption_by_sector.csv"
        part_file.rename(final_file)

        # Delete _SUCCESS
        success = output_path / "_SUCCESS"
        if success.exists():
            success.unlink()

    def run(self):
        df = self.read_inputs()
        df = self.transform(df)
        self.write(df)
