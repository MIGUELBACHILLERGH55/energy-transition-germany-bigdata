# Execute EEA pipeline to ensure its correct functioning

from src.config.loader import config
from pyspark.sql import SparkSession
from src.transform.sources.eea.pipeline import EeaTransformerPipeline

proj_config = config.project_config
eea_source = config.sources["eea"]
spark_session = SparkSession.builder.getOrCreate()


eea_pipeline = EeaTransformerPipeline(spark_session, proj_config, eea_source)
eea_pipeline.run()
