from pyspark.sql import DataFrame
from src.transform.core.pipelines.batch_transformer import BatchTransformerPipeline


class AgebTransformerPipeline(BatchTransformerPipeline):
    def apply_steps(self, ds_name: str, df: DataFrame) -> DataFrame:
        print("THis is working my g")
        pass
