from src.config.loader import config, spark_session
from src.extract.core.extractors.file_extractor import FileExtractor

proj_config = config.project_config
ageb_source = config.sources["ageb"]

if __name__ == "__main__":
    fe_ageb = FileExtractor(proj_config, ageb_source, spark_session)
    fe_ageb.run()
