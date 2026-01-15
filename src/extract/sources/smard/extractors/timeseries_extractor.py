from src.config.models.project_models import ProjectConfig
from src.config.models.source_models import SourceSpec
from extract.core.strategies.downloader_base import BaseDownloader
from src.extract.core.extractors.batch_extractor import BatchExtractor
from src.extract.sources.smard.downloaders.timeseries_downloader import (
    SmardTimeseriesDownloader,
)
from datetime import date, timedelta, time, datetime
from typing import Type


# Different downloader my guy, and probably a diff location as well
class SmardTimeseriesExtractor(BatchExtractor):
    downloader_cls: Type[BaseDownloader] = SmardTimeseriesDownloader

    def __init__(
        self,
        project_config: ProjectConfig,
        source: SourceSpec,
        run_date: date | None = None,
    ):
        super().__init__(
            project_config=project_config,
            source=source,
            downloader_cls=self.downloader_cls,
            run_date=run_date,
        )


# Plan
# read available_indices for that dataset
# cut wiht start/end
# generate a PlanItem

# SmardTimeseriesExtractor
# receibes this and downloades the json everthin goood
