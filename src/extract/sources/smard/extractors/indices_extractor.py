from src.extract.core.extractors.batch_extractor import BatchExtractor
from src.extract.sources.smard.downloaders.indices_downloader import (
    SmardIndicesDownloader,
)
from src.config.models.project_models import ProjectConfig
from src.config.models.source_models import SourceSpec
from src.extract.core.strategies.downloader_base import BaseDownloader
from src.extract.core.planning.plan_item import PlanItem
from datetime import date, timedelta, time, datetime
from src.io.path_resolver import resolve_input_path, resolve_output_path
from typing import Type


# Different downloader my guy, and probably a diff location as well
class SmardIndicesExtractor(BatchExtractor):
    downloader_cls: Type[BaseDownloader] = SmardIndicesDownloader

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

    def plan(self) -> list[PlanItem]:
        source_name = self.source.name
        plan_item_list = []
        for ds_name, dataset_cfg in self.source.datasets.items():
            pi = PlanItem(
                source_name=source_name,
                dataset_name=dataset_cfg.name,
                dataset_id=dataset_cfg.metadata.dataset_id,
                start_ts=datetime.combine(self.effective_date, time(0, 0)),
                end_ts=datetime.combine(self.effective_date, time(23, 0)),
                request_params=dataset_cfg.request,
                output_path=resolve_output_path(
                    self.project_config,
                    dataset_cfg,
                    "landing",
                ),
                input_format=dataset_cfg.storage["format"],
            )
            plan_item_list.append(pi)
        return plan_item_list
