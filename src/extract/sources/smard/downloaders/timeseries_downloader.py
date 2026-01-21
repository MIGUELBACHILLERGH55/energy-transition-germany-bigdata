from dataclasses import dataclass
from src.extract.core.strategies.downloader_base import BaseDownloader
from src.extract.core.planning.timestamp_task import TimestampExtractionTask
from src.io.http import fetch_json

from src.extract.sources.smard.parsers.timeseries import parse_timeseries_response
from src.extract.sources.smard.models.endpoint import SmardTimeseriesEndpoint
from src.extract.sources.smard.endpoints.builders import (
    build_time_series_data_endpoint,
)


@dataclass
class SmardTimeseriesDownloader(BaseDownloader):
    def prepare(self, task: TimestampExtractionTask):
        # 1. Prepare the endpoint
        self.filter = task.request_params["filter"]
        self.resolution = task.request_params["resolution"]

        # Set use_last_available flag
        self.use_last_available = task.use_last_available

        # Save start_date and end_date
        self.start_date = task.start_date
        self.end_date = task.end_date

        endpoint = SmardTimeseriesEndpoint(
            base_endpoint=self.base_url,
            filter=self.filter,
            resolution=self.resolution,
            timestamp_ts=str(task.timestamp_ms),
        )
        endpoint_str = build_time_series_data_endpoint(endpoint)

        self.endpoint = endpoint_str

        # 2. Resolve the ouput path here too
        self.output_path = task.output_path

    def download(self):
        response = fetch_json(self.endpoint)

        # Parse the payload and save it to self.output_path
        run_date_str = self.run_date.isoformat()

        parsed_payload = parse_timeseries_response(
            filter_name=self.dataset_name,
            filter_value=self.filter,
            resolution=self.resolution,
            run_date=run_date_str,
            response=response,
            start_date=self.start_date,
            end_date=self.end_date,
            mode="last_available" if self.use_last_available else "range",
        )

        if self.use_last_available:
            self.data_date = parsed_payload["meta"]["data_date"]
            self.file_name = (
                f"{self.dataset_name}_"
                f"{self.resolution}_"
                f"data_date={self.data_date}_"
                f"run={self.run_date}.json"
            )

        return parsed_payload

    def fetch(self, task: TimestampExtractionTask):
        self.prepare(task)
        return self.download()
