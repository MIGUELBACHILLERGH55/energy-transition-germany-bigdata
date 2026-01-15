# src/extract/core/extractors/batch_extractor.py
from src.config.loader import ProjectConfig
from src.config.models.source_models import SourceSpec, DatasetSpec
from src.extract.core.planning.plan_item import PlanItem
from src.io.path_resolver import resolve_layer_root
from src.config.paths import PROJECT_ROOT
import requests
from datetime import date, timedelta, time, datetime
from src.extract.core.strategies.downloader_base import BaseDownloader
from typing import Type

"""
Batch Extractor
---------------

Defines the orchestration flow for batch-mode data extraction.
Implements the Template Method pattern: delegates logic to strategies
while maintaining a consistent execution sequence.

Responsibilities:
- Coordinate the full extraction lifecycle:
  1. prepare() → setup sessions, headers, paths
  2. plan() → determine units of work (PlanItem list)
  3. fetch() → retrieve raw data via DownloaderStrategy
  1-3: run() -> run full extraction lifecycle
- Ensure idempotent and profile-aware persistence.
- Handle error reporting and orchestration-level metrics.

This module contains no protocol-specific logic — all details are delegated
to injected strategy classes.
"""


class BatchExtractor:
    def __init__(
        self,
        project_config: ProjectConfig,
        source: SourceSpec,
        downloader_cls: Type[BaseDownloader],
        run_date: date | None = None,
    ):
        self.project_config = project_config
        self.source = source
        self.downloader_cls = downloader_cls
        self.run_date = run_date or date.today()
        self.safety_lag_days = source.availability_lag_days
        self.effective_date = self.run_date - timedelta(days=self.safety_lag_days)

    def prepare(self):
        active_env = self.project_config.active_env
        env_profile = self.project_config.env_profiles[active_env].bronze
        storage_profile = self.project_config.profiles.get(env_profile)

        self.active_env = active_env

        self.storage_profile = storage_profile

        if self.source.kind == "api":
            session = requests.Session()
            base_url = self.source.base_url
            retry = self.source.retry
            timeout_s = self.source.timeout_s
            self.downloader = self.downloader_cls(
                session, base_url, timeout_s, retry, self.run_date
            )

        else:
            self.session = None

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
                output_path=dataset_cfg.destinations["bronze"].path,
                input_format=dataset_cfg.storage["format"],
            )
            plan_item_list.append(pi)
        return plan_item_list

    def fetch(self, pi: PlanItem):
        # create a downloader and init it with
        # session,base_url, timeout_s, retry
        # for plan_item in list_plan_items:
        #     downloader.download(plan_item)
        self.downloader.fetch(pi)

    def run(self):
        self.prepare()
        items = self.plan()
        for pi in items:
            self.fetch(pi)
