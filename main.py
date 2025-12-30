# Execute EEA pipeline to ensure its correct functioning

from src.config.loader import config
from pyspark.sql import SparkSession
from src.transform.sources.ageb.pipeline import AgebTransformerPipeline
from src.extract.core.extractors.file_extractor import FileExtractor


proj_config = config.project_config
ageb_source = config.sources["ageb"]
spark_session = SparkSession.builder.getOrCreate()

fe = FileExtractor(proj_config, ageb_source, spark_session)
fe.run()
# ageb_pipeline = AgebTransformerPipeline(spark_session, proj_config, ageb_source)
# ageb_pipeline.run()
