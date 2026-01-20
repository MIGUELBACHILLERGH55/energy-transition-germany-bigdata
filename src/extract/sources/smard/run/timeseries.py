from src.config.loader import config
from src.extract.sources.smard.extractors.timeseries_extractor import (
    SmardTimeseriesExtractor,
)

proj_config = config.project_config
smard_source = config.sources["smard"]

if __name__ == "__main__":
    smard_timeseries_extractor = SmardTimeseriesExtractor(proj_config, smard_source)

    smard_timeseries_extractor.run()
