from src.transform.sources.smard.pipeline import SmardTimeseriesPipeline
from src.config.loader import config, spark_session

proj_config = config.project_config
opsd_source = config.sources["smard"]

if __name__ == "__main__":
    smard_pipeline = SmardTimeseriesPipeline(spark_session, proj_config, opsd_source)
    smard_pipeline.run()
