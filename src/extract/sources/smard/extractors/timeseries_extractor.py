from src.config.models.project_models import ProjectConfig
from src.config.models.source_models import SourceSpec
from src.extract.sources.smard.planner.timeseries_planner import SmardTimeseriesPlanner
from src.extract.core.strategies.downloader_base import BaseDownloader
from src.extract.core.extractors.batch_extractor import BatchExtractor
from src.extract.core.planning.timestamp_task import TimestampExtractionTask
from src.extract.sources.smard.downloaders.timeseries_downloader import (
    SmardTimeseriesDownloader,
)
from datetime import date
from typing import Type

from src.io.path_resolver import resolve_output_path


# Different downloader my guy, and probably a diff location as well
class SmardTimeseriesExtractor(BatchExtractor):
    downloader_cls: Type[BaseDownloader] = SmardTimeseriesDownloader

    def __init__(
        self,
        project_config: ProjectConfig,
        source: SourceSpec,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        super().__init__(
            project_config=project_config,
            source=source,
            downloader_cls=self.downloader_cls,
            start_date=start_date,
            end_date=end_date,
        )

    def plan(self) -> list[TimestampExtractionTask]:
        list_timestamp_tasks = []

        for ds_name, dataset_cfg in self.source.datasets.items():
            timeseries_planner = SmardTimeseriesPlanner(
                start_date=self.start_date,
                end_date=self.end_date,
                av_indices_path=resolve_output_path(
                    self.project_config, dataset_cfg, "landing"
                ),
                source_name=self.source.name,
                dataset_name=dataset_cfg.name,
                output_path=resolve_output_path(
                    self.project_config, dataset_cfg, "bronze"
                ),
                run_date=self.run_date,
                request_params=dataset_cfg.request,
            )
            list_timestamp_tasks.extend(timeseries_planner.plan())

        return list_timestamp_tasks
