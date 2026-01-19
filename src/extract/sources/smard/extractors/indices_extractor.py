from src.extract.core.extractors.batch_extractor import BatchExtractor
from src.extract.core.planning.index_task import IndexExtractionTask
from src.extract.core.planning.task import ExtractionTask
from src.extract.sources.smard.downloaders.indices_downloader import (
    SmardIndicesDownloader,
)
from src.config.models.project_models import ProjectConfig
from src.config.models.source_models import SourceSpec
from src.extract.core.strategies.downloader_base import BaseDownloader
from datetime import time, datetime
from src.io.path_resolver import resolve_input_path, resolve_output_path
from typing import Type


# Different downloader my guy, and probably a diff location as well
class SmardIndicesExtractor(BatchExtractor):
    downloader_cls: Type[BaseDownloader] = SmardIndicesDownloader

    def __init__(
        self,
        project_config: ProjectConfig,
        source: SourceSpec,
    ):
        super().__init__(
            project_config=project_config,
            source=source,
            downloader_cls=self.downloader_cls,
            start_date=None,
            end_date=None,
        )

    def plan(self) -> list[ExtractionTask]:
        source_name = self.source.name
        index_extraction_tasks_list = []
        for ds_name, dataset_cfg in self.source.datasets.items():
            index_extraction_task = IndexExtractionTask(
                source_name=source_name,
                dataset_name=dataset_cfg.name,
                request_params=dataset_cfg.request,
                output_path=resolve_output_path(
                    self.project_config, dataset_cfg, "landing"
                ),
            )
            index_extraction_tasks_list.append(index_extraction_task)
        return index_extraction_tasks_list
