from dataclasses import dataclass
from src.extract.core.strategies.downloader_base import BaseDownloader
from src.extract.core.planning.timestamp_task import TimestampExtractionTask
from src.io.json import write_json
from src.io.http import fetch_json

from src.extract.sources.smard.parsers.timeseries import parse_timeseries_response
from src.extract.sources.smard.models.endpoint import SmardTimeseriesEndpoint
from src.extract.sources.smard.endpoints.builders import (
    build_time_series_data_endpoint,
)
from pprint import pprint


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

        # 3. Save the file name
        self.dataset_name = task.dataset_name
        if self.start_date and self.end_date:
            self.file_name = f"{self.dataset_name}_{self.resolution}_{self.start_date}_{self.end_date}_{self.run_date}.json"
        else:
            # Effective date
            self.file_name = (
                f"{self.dataset_name}_{self.resolution}_{self.run_date}.json"
            )

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

        write_json(parsed_payload, self.output_path, self.file_name)

    def fetch(self, task: TimestampExtractionTask):
        self.prepare(task)
        self.download()
