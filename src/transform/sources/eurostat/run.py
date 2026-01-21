from src.transform.sources.eurostat.pipeline import EurostatTransformerPipeline
from src.config.loader import config, spark_session

proj_config = config.project_config
eurostat_source = config.sources["eurostat"]

if __name__ == "__main__":
    eurostat_pipeline = EurostatTransformerPipeline(
        spark_session, proj_config, eurostat_source
    )
    eurostat_pipeline.run()
