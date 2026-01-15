# energy-transition-germany-bigdata/src/extract/exploration/smard/times_series/helpers.py
from pathlib import Path
from itertools import islice
from pprint import pprint
from src.extract.sources.smard.models.endpoint import (
    SmardIndicesEndpoint,
    SmardTimeseriesEndpoint,
)

from src.extract.sources.smard.endpoints.builders import (
    build_time_series_data_endpoint,
    build_indices_endpoint,
    ts_to_datetime,
)
from src.io.http import fetch_json
from src.io.json import write_json

CURRENT_DIR = Path(__file__).resolve().parent


def smard_time_series_exploration(
    resolutions_to_explore: list[str],
    filters_to_explore: dict[str, int],
    verbose: bool = False,
    save: bool = False,
    output_dir: Path | None = None,
):
    for resolution in resolutions_to_explore:
        for filter_name, filter_value in filters_to_explore.items():
            indices_endpoint = SmardIndicesEndpoint(
                "https://www.smard.de/app", filter_value, resolution
            )
            endpoint = build_indices_endpoint(indices_endpoint)

            data = fetch_json(endpoint)

            list_timestamps_ms = data["timestamps"]

            summary = build_time_series_summary(
                filter_name,
                filter_value,
                resolution,
                list_timestamps_ms,
                max_calls=5,
                max_records_per_call=5,
            )

            if save:
                write_json(
                    summary,
                    output_dir=output_dir
                    or CURRENT_DIR / "time_series_metadata_summaries",
                    file_name=f"{filter_name}_{resolution}_time_series_summary.json",
                )

            if verbose:
                print(
                    f"---------- Exploring Smard Time Series Endpoint: ------------ \n {endpoint} \n"
                )
                print(
                    f"Exploring a snippet of {filter_name} with resolution={resolution} from {summary['snippet_date_range']}: \n"
                )

                pprint(summary)

                print()


def build_time_series_summary(
    filter_name: str,
    filter_value: int,
    resolution: str,
    list_timestamps_ms: list[int],
    max_calls: int = 5,
    max_records_per_call: int = 5,
) -> dict:
    """
    Build a lightweight summary of the available time-series metadata and
    sample values retrieved from the SMARD API.

    The returned dictionary has the form:

        {
            "filter_name": str,
            "filter_value": int,
            "resolution": str,
            "total_timestamps": int,
            "data_range": {
                "min": str,  # ISO 8601, UTC
                "max": str,  # ISO 8601, UTC
            },
            "snippet_date_range": str,
            "snippet": [
                [iso_timestamp: str, timestamp_ms: int, value: float | None]
            ],
        }

    Args:
        filter_name (str): Human readable name of the filter
            (e.g. "nuclear_energy").
        filter_value (int): Integer code used by the SMARD API for this filter.
        resolution (str): Timestamp resolution (e.g. "hour", "quarterhour").
        list_timestamps_ms (list[int]): List of timestamps in milliseconds
            returned by the index API.
        max_calls (int): Maximum number of API requests allowed when fetching
            sample values for the snippet.
        max_records_per_call (int): Maximum number of data records to keep from
            each API response when building the snippet.

    Returns:
        dict: A dictionary summarizing the available timestamps (count and
        date range) and a small snippet of time-series values.
    """
    list_timestamps_datetime_utc = [
        ts_to_datetime(ts_ms) for ts_ms in list_timestamps_ms
    ]

    min_date = min(list_timestamps_datetime_utc).isoformat()
    max_date = max(list_timestamps_datetime_utc).isoformat()

    snippet = []

    for ts in islice(list_timestamps_ms, max_calls):
        time_series_endpoint = SmardTimeseriesEndpoint(
            "https://www.smard.de/app",
            filter=filter_value,
            resolution=resolution,
            timestamp_ts=str(ts),
        )

        time_series_endpoint = SmardTimeseriesEndpoint(
            "https://www.smard.de/app", filter_value, resolution, timestamp_ts=str(ts)
        )

        time_series_endpoint_str = build_time_series_data_endpoint(time_series_endpoint)
        data = fetch_json(time_series_endpoint_str)

        for record in data["series"][:max_records_per_call]:
            snippet.append(
                [
                    ts_to_datetime(record[0]).isoformat(),
                    record[0],
                    record[1],
                ]
            )

    if snippet:
        snippet_start = snippet[0][0]
        snippet_end = snippet[-1][0]
        snippet_date_range_str = f"({snippet_start}) - ({snippet_end})"
    else:
        snippet_date_range_str = ""

    d = {}
    d["filter_name"] = filter_name
    d["filter_value"] = filter_value
    d["resolution"] = resolution
    d["total_timestamps"] = len(list_timestamps_datetime_utc)
    d["data_range"] = {"min": min_date, "max": max_date}
    d["snippet_date_range"] = snippet_date_range_str
    d["snippet"] = snippet

    return d
