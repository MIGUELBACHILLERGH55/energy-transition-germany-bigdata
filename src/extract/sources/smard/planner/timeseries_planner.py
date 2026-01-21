from src.extract.core.planning.timestamp_task import TimestampExtractionTask
from datetime import date, time, timezone, datetime
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
        verbose: bool = False,
    ):
        self.av_indices_path = next(av_indices_path.iterdir())
        self.run_date = run_date
        self.output_path = output_path
        self.dataset_name = dataset_name
        self.source_name = source_name
        self.request_params = request_params
        self.verbose = verbose

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
            datetime.fromtimestamp(ts / 1000, tz=timezone.utc).date()
            for ts in self.data["timestamps_ms"]
        ]

        self.anchor_date = converted_ts
        self.timestamps_ms = self.data["timestamps_ms"]

        if self.verbose:
            print(
                f"[SMARD planner] first={self.anchor_date[0]} "
                f"last={self.anchor_date[-1]} "
                f"total={len(self.anchor_date)}"
            )

    def plan(self):
        self.read_json()
        self.prepare()
        tasks: list[TimestampExtractionTask] = []

        if self.start_date is None and self.end_date is None:
            for index, anchor_date in enumerate(self.anchor_date):
                tasks.append(
                    TimestampExtractionTask(
                        timestamp_ms=self.timestamps_ms[index],
                        source_name=self.source_name,
                        dataset_name=self.dataset_name,
                        output_path=self.output_path,
                        request_params=self.request_params,
                        use_last_available=False,
                        start_date=self.start_date,
                        end_date=self.end_date,
                    )
                )
            return tasks

        # Start date and download all data until the last record
        if self.start_date and self.end_date is None:
            for index, anchor_date in enumerate(self.anchor_date):
                if anchor_date >= self.start_date:
                    tasks.append(
                        TimestampExtractionTask(
                            timestamp_ms=self.timestamps_ms[index],
                            source_name=self.source_name,
                            dataset_name=self.dataset_name,
                            output_path=self.output_path,
                            request_params=self.request_params,
                            start_date=self.start_date,
                        )
                    )
            return tasks

        # closed range
        if self.start_date and self.end_date:
            for idx, anchor_date in enumerate(self.anchor_date):
                if self.start_date <= anchor_date <= self.end_date:
                    tasks.append(
                        TimestampExtractionTask(
                            timestamp_ms=self.timestamps_ms[idx],
                            source_name=self.source_name,
                            dataset_name=self.dataset_name,
                            output_path=self.output_path,
                            request_params=self.request_params,
                            start_date=self.start_date,
                            end_date=self.end_date,
                        )
                    )

        return tasks
