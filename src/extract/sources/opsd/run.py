from src.config.loader import config, spark_session
from src.extract.core.extractors.file_extractor import FileExtractor

proj_config = config.project_config
opsd_source = config.sources["opsd"]

if __name__ == "__main__":
    fe_opsd = FileExtractor(proj_config, opsd_source, spark_session)
    fe_opsd.run()
