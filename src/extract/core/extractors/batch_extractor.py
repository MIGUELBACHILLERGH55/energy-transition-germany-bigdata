# src/extract/core/extractors/batch_extractor.py
from abc import abstractclassmethod, abstractmethod
from typing import BinaryIO

from pyspark.sql import SparkSession
from src.config.loader import config, ProjectConfig
from src.config.models.source_models import SourceSpec, DatasetSpec
from src.extract.core.planning.plan_item import PlanItem
from src.io.path_resolver import resolve_layer_root
from src.config.paths import PROJECT_ROOT

from datetime import date, timedelta, time, datetime
from pprint import pprint
import requests
from src.extract.core.strategies.downloader_base import BaseDownloader

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
  4. parse() → transform raw payload via ParserStrategy
  5. persist_landing() → write cleaned data via StorageClient
  6. report() → summarize metrics and results
- Ensure idempotent and profile-aware persistence.
- Handle error reporting and orchestration-level metrics.

This module contains no protocol-specific logic — all details are delegated
to injected strategy classes.
"""


class BatchExtractor:
    def __init__(
        self,
        spark_session: SparkSession,
        project_config: ProjectConfig,
        source: SourceSpec,
        downloader,
        parser,
        run_date: date | None = None,
    ):
        self.project_config = project_config
        self.source = source
        self.downloader = downloader
        self.parser = parser
        self.run_date = run_date or date.today()
        self.safety_lag_days = source.availability_lag_days
        self.effective_date = self.run_date - timedelta(days=self.safety_lag_days)

    def prepare(self):
        active_env = self.project_config.active_env
        env_profile = self.project_config.env_profiles[active_env].bronze
        storage_profile = self.project_config.profiles.get(env_profile)

        self.active_env = active_env
        self.storage_profile = storage_profile

        self.bronze_root = resolve_layer_root(self.project_config, "bronze")

        if self.source.kind == "api":
            session = requests.Session()
            base_url = self.source.base_url
            retry = self.source.retry
            timeout_s = self.source.timeout_s
            self.downloader = self.downloader(session, base_url, timeout_s, retry)

        else:
            self.session = None

    def plan(self) -> list[PlanItem]:
        source_name = self.source.name
        l = []
        for ds_name, ds_cfg in self.source.datasets.items():
            pi = PlanItem(
                source_name=source_name,
                dataset_name=ds_cfg.name,
                dataset_id=ds_cfg.metadata.dataset_id,
                start_ts=datetime.combine(self.effective_date, time(0, 0)),
                end_ts=datetime.combine(self.effective_date, time(23, 0)),
                request_params=ds_cfg.request,
                output_path=ds_cfg.destinations["bronze"].path,
            )
            l.append(pi)
        return l

    @abstractmethod
    def fetch(self):
        # create a downloader and init it with
        # session,base_url, timeout_s, retry
        # for plan_item in list_plan_items:
        #     downloader.download(plan_item)
        pass

    def parse(self):
        pass

    def presist_landing(self):
        pass

    def report(self):
        pass


project_config = config.project_config
smard_source = config.sources["smard"]

extractor = BatchExtractor(project_config, smard_source, BaseDownloader, None, None)
extractor.prepare()
extractor.plan()
