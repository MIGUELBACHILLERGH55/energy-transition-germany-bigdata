from pyspark.sql import DataFrame, SparkSession
from src.transform.core.pipelines.batch_transformer import BatchTransformerPipeline

from src.config.loader import config


class OpsdTransformerPipeline(BatchTransformerPipeline):
    def apply_steps(self, ds_name: str, df: DataFrame) -> DataFrame:
        df.show(n=5, truncate=False)
        return df

    def run(self) -> None:
        print("Using this custom bitch")
        bronze_paths = self.read_bronze_paths()

        for ds_name, bronze_path in bronze_paths.items():
            df = self.read_bronze(bronze_path)
            df2 = self.apply_steps(ds_name, df)


spark_sesion = SparkSession.builder.getOrCreate()
opsd_source = config.sources["opsd"]

OpsdTransformerPipeline(spark_sesion, config.project_config, opsd_source).run()
