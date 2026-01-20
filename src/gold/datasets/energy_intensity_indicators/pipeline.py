from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as sf
from src.gold.io.paths import resolve_gold_dataset_path
from src.io.path_resolver import resolve_output_path
from src.config.loader import config
from src.gold.datasets.energy_intensity_indicators.mappings import (
    INDICATOR_GROUP_MAP,
    INDICATOR_LABEL_MAP,
    INDICATOR_SCOPE_MAP,
)
from pathlib import Path


class EnergyIntensityIndicators:
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
        df = df.filter("table_id IN (7.1)")
        return df

    def transform(self, df: DataFrame) -> DataFrame:
        # Do some things here
        df = df.withColumn("dataset", sf.lit("energy_intensity_indicators"))

        df = df.withColumn(
            "indicator_label",
            sf.create_map([sf.lit(x) for x in sum(INDICATOR_LABEL_MAP.items(), ())])[
                sf.col("dimension")
            ],
        )

        df = df.withColumn(
            "indicator_group",
            sf.create_map([sf.lit(x) for x in sum(INDICATOR_GROUP_MAP.items(), ())])[
                sf.col("dimension")
            ],
        )

        df = df.withColumn(
            "indicator_scope",
            sf.create_map([sf.lit(x) for x in sum(INDICATOR_SCOPE_MAP.items(), ())])[
                sf.col("dimension")
            ],
        )

        return df

    def write(self, df: DataFrame):
        output_path: Path = resolve_gold_dataset_path("energy_intensity_indicators")
        (
            df.coalesce(1)
            .write.mode("overwrite")
            .option("header", "true")
            .option("delimiter", ",")
            .csv(output_path.as_posix())
        )

        # Find the part file and rename it
        part_file = next(output_path.glob("part*.csv"))

        final_file = output_path / "energy_intensity_indicators.csv"
        part_file.rename(final_file)

        # Delete _SUCCESS
        success = output_path / "_SUCCESS"
        if success.exists():
            success.unlink()

    def run(self):
        df = self.read_inputs()
        df = self.transform(df)
        self.write(df)
