# Execute EEA pipeline to ensure its correct functioning

from src.config.loader import config
from pyspark.sql import SparkSession
from src.transform.sources.opsd.pipeline import OpsdTransformerPipeline


proj_config = config.project_config
opsd_source = config.sources["opsd"]
spark_session = SparkSession.builder.getOrCreate()

opsd_pipeline = OpsdTransformerPipeline(spark_session, proj_config, opsd_source)
opsd_pipeline.run()
