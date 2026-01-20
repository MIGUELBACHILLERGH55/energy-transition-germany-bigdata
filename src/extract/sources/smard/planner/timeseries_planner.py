from src.extract.core.planning.timestamp_task import TimestampExtractionTask
from datetime import date
import json


class SmardTimeseriesPlanner:
    def __init__(
        self,
        av_indices_path,
        start_date,
        end_date,
        source_name,
        dataset_name,
        output_path,
        run_date: date,
        request_params,
    ):
        self.av_indices_path = next(av_indices_path.iterdir())
        self.run_date = run_date
        self.output_path = output_path
        self.dataset_name = dataset_name
        self.source_name = source_name
        self.request_params = request_params

        # User input
        self.start_date = start_date
        self.end_date = end_date

    def read_json(self):
        # This should be a heper
        with open(self.av_indices_path) as f:
            data = json.load(f)

        self.data = data

    def prepare(self):
        # Make sure the convert_ts_ms_to_datetime is available here, this helper
        converted_ts = [
            date.fromtimestamp(ts / 1000) for ts in self.data["timestamps_ms"]
        ]
        self.anchor_date = converted_ts
        self.timestamps_ms = self.data["timestamps_ms"]

    def plan(self):
        self.read_json()
        self.prepare()
        list_timestamp_tasks = []

        if self.start_date is None and self.end_date is None:
            task = TimestampExtractionTask(
                timestamp_ms=self.timestamps_ms[-1],
                source_name=self.source_name,
                dataset_name=self.dataset_name,
                output_path=self.output_path,
                request_params=self.request_params,
                use_last_available=True,
                start_date=self.start_date,
                end_date=self.end_date,
            )
            list_timestamp_tasks.append(task)

        if self.start_date and self.end_date:
            for index, anchor_date in enumerate(self.anchor_date):
                if self.start_date <= anchor_date <= self.end_date:
                    task = TimestampExtractionTask(
                        timestamp_ms=self.timestamps_ms[index],
                        source_name=self.source_name,
                        dataset_name=self.dataset_name,
                        output_path=self.output_path,
                        request_params=self.request_params,
                        start_date=self.start_date,
                        end_date=self.end_date,
                    )
                    list_timestamp_tasks.append(task)

        return list_timestamp_tasks
