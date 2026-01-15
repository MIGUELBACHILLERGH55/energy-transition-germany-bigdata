from src.transform.sources.ageb.pipeline import AgebTransformerPipeline
from src.config.loader import config, spark_session

proj_config = config.project_config
ageb_source = config.sources["ageb"]

if __name__ == "__main__":
    ageb_pipeline = AgebTransformerPipeline(spark_session, proj_config, ageb_source)
    ageb_pipeline.run()
