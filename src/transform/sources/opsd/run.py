from src.transform.sources.opsd.pipeline import OpsdTransformerPipeline
from src.config.loader import config, spark_session

proj_config = config.project_config
opsd_source = config.sources["opsd"]

if __name__ == "__main__":
    opsd_pipeline = OpsdTransformerPipeline(spark_session, proj_config, opsd_source)
    opsd_pipeline.run()
