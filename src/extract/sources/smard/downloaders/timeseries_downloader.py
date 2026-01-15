from dataclasses import dataclass
from src.extract.core.strategies.downloader_base import BaseDownloader
from src.extract.core.planning.plan_item import PlanItem
from src.io.json import write_json
from src.io.http import fetch_json

from src.extract.sources.smard.models.endpoint import SmardTimeseriesEndpoint
from src.extract.sources.smard.endpoints.builders import (
    build_time_series_data_endpoint_json,
)


@dataclass
class SmardTimeseriesDownloader(BaseDownloader):
    def prepare(self, pi: PlanItem):
        # 1. Prepare the endpoint
        self.filter = pi.request_params["filter"]
        self.resolution = pi.request_params["resolution"]

        endpoint = SmardIndicesEndpoint(
            base_endpoint=self.base_url,
            filter=self.filter,
            resolution=self.resolution,
        )

        endpoint_str = build_indices_endpoint(endpoint)

        self.endpoint = endpoint_str

        # 2. Resolve the ouput path here too
        self.output_path = pi.output_path

        # 3. Save the file name
        self.dataset_name = pi.dataset_name
        self.file_name = f"{self.dataset_name}_available_indices_{self.resolution}_{self.run_date}.json"

    def download(self):
        response = fetch_json(self.endpoint)

        # Parse the payload and save it to self.output_path
        run_date_str = self.run_date.isoformat()
        parsed_payload = parse_available_indices_response(
            self.dataset_name, self.filter, self.resolution, run_date_str, response
        )
        write_json(parsed_payload, self.output_path, self.file_name)

    def fetch(self, pi: PlanItem):
        self.prepare(pi)
        self.download()
