from src.config.loader import config, spark_session
from src.extract.core.extractors.file_extractor import FileExtractor

proj_config = config.project_config
eurostat_source = config.sources["eurostat"]

if __name__ == "__main__":
    fe_eurostat = FileExtractor(proj_config, eurostat_source, spark_session)
    fe_eurostat.run()
