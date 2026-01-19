# src/extract/core/extractors/batch_extractor.py
from abc import abstractmethod
from src.config.loader import ProjectConfig
from src.config.models.source_models import SourceSpec, DatasetSpec
from src.io.path_resolver import resolve_layer_root
from src.config.paths import PROJECT_ROOT
import requests
from datetime import date, timedelta, time, datetime
from src.extract.core.strategies.downloader_base import BaseDownloader
from typing import Type
from src.extract.core.planning.task import ExtractionTask

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
        start_date: date | None,
        end_date: date | None,
    ):
        self.project_config = project_config
        self.source = source
        self.downloader_cls = downloader_cls
        self.run_date = date.today()
        self.start_date = start_date
        self.end_date = end_date
        self.safety_lag_days = source.availability_lag_days

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

    @abstractmethod
    def plan(self) -> list[ExtractionTask]:
        pass

    def fetch(self, task: ExtractionTask):
        # create a downloader and init it with
        # session,base_url, timeout_s, retry
        # for plan_item in list_plan_items:
        #     downloader.download(plan_item)
        self.downloader.fetch(task)

    def run(self):
        self.prepare()
        items = self.plan()
        for task in items:
            self.fetch(task)
