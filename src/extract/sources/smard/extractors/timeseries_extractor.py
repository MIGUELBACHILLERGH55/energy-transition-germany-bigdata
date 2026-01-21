from src.config.models.project_models import ProjectConfig
from src.config.models.source_models import SourceSpec
from src.extract.sources.smard.planner.timeseries_planner import SmardTimeseriesPlanner
from src.extract.core.strategies.downloader_base import BaseDownloader
from src.extract.core.extractors.batch_extractor import BatchExtractor
from src.extract.core.planning.timestamp_task import TimestampExtractionTask
from src.extract.sources.smard.downloaders.timeseries_downloader import (
    SmardTimeseriesDownloader,
)
from src.io.json import write_json
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
        verbose: bool = False,
    ):
        super().__init__(
            project_config=project_config,
            source=source,
            downloader_cls=self.downloader_cls,
            start_date=start_date,
            end_date=end_date,
        )
        self.verbose = verbose

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
                verbose=self.verbose,
            )
            list_timestamp_tasks.extend(timeseries_planner.plan())

        return list_timestamp_tasks

    def write_final_output(self, payload: dict, task: TimestampExtractionTask):
        dataset = task.dataset_name
        resolution = task.request_params["resolution"]

        if task.start_date and task.end_date:
            file_name = (
                f"{dataset}_{resolution}_"
                f"range={task.start_date}_{task.end_date}_"
                f"run={self.run_date}.json"
            )
        elif task.start_date:
            file_name = (
                f"{dataset}_{resolution}_"
                f"from={task.start_date}_"
                f"run={self.run_date}.json"
            )
        else:
            file_name = f"{dataset}_{resolution}_run={self.run_date}.json"

        write_json(payload, task.output_path, file_name)

        if self.verbose:
            print(
                f"[SMARD extractor] Written single file: {file_name} "
                f"with {len(payload['data'])} points"
            )

    def run(self):
        self.prepare()
        tasks = self.plan()

        from collections import defaultdict

        tasks_by_dataset = defaultdict(list)

        for task in tasks:
            tasks_by_dataset[task.dataset_name].append(task)

        for dataset_name, dataset_tasks in tasks_by_dataset.items():
            all_data = []
            meta = None

            for task in dataset_tasks:
                payload = self.downloader.fetch(task)

                if not payload or "data" not in payload:
                    continue

                if meta is None:
                    meta = payload.get("meta", {})

                all_data.extend(payload["data"])

            if not all_data:
                print(f"[SMARD extractor] No data for dataset {dataset_name}")
                continue

            final_payload = {
                "meta": meta,
                "data": all_data,
            }

            self.write_final_output(final_payload, dataset_tasks[0])
