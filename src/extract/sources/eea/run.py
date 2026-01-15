from src.config.loader import config, spark_session
from src.extract.core.extractors.file_extractor import FileExtractor

proj_config = config.project_config
eea_source = config.sources["eea"]

if __name__ == "__main__":
    fe_eea = FileExtractor(proj_config, eea_source, spark_session)
    fe_eea.run()
