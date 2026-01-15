from src.transform.sources.eea.pipeline import EeaTransformerPipeline
from src.config.loader import config, spark_session

proj_config = config.project_config
eea_source = config.sources["eea"]

if __name__ == "__main__":
    eea_pipeline = EeaTransformerPipeline(spark_session, proj_config, eea_source)
    eea_pipeline.run()
