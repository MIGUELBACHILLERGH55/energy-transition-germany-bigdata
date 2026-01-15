from pathlib import Path
from ..constants import base_smard_endpoint
from ..helpers import build_indices_endpoint, ts_to_datetime
from ...helpers import save_summary_to_json
from src.io.http import fetch_json
from pprint import pprint

CURRENT_DIR = Path(__file__).resolve().parent


def smard_indices_exploration(
    resolutions_to_explore: list[str],
    filters_to_explore: dict[str, int],
    include_or_list: bool = True,
    verbose: bool = False,
    save: bool = False,
    output_dir: Path | None = None,
):
    for resolution in resolutions_to_explore:
        for filter_name, filter_value in filters_to_explore.items():
            indices_endpoint = base_smard_endpoint._replace(
                filter=filter_value, resolution=resolution
            )
            endpoint = build_indices_endpoint(indices_endpoint)

            data = fetch_json(endpoint)

            list_timestamps_ms = data["timestamps"]

            summary = build_indices_summary(
                filter_name,
                filter_value,
                resolution,
                list_timestamps_ms,
                include_or_list=include_or_list,
            )

            if save:
                save_summary_to_json(
                    summary,
                    output_dir=output_dir or CURRENT_DIR / "indices_metadata_summaries",
                    file_name=f"{filter_name}_{resolution}_indices_summary.json",
                )

            if verbose:
                print(
                    f"---------- Exploring Smard Indices Series Endpoint: ------------ \n {endpoint} \n"
                )
                print(f"{filter_name} with resolution: {indices_endpoint.resolution}")
                pprint(summary)
                print()


def build_indices_summary(
    filter_name: str,
    filter_value: int,
    resolution: str,
    list_timestamps_ms: list[int],
    include_or_list: bool = True,
) -> dict:
    """Build a structured summary of the index metadata.

    The returned dictionary contains:


    {
        "filter_name": str,
        "filter_value": int,
        "resolution": str,
        "total_timestamps": int,
        "data_range": {
            "min": datetime,
            "max": datetime,
        },
        "years": {
            "2020": "full",
            "2021": "missing months 3,4,6",
            "2022": :no data",
        },
        "original_list_ms": [1237483, 1912837, ...]

    }

    Args:
        filter_name (str): Human readable name of the filter (e.g. "nuclear_energy").
        filter_value (int): Integer code used by the SMARD API for this filter.
        resolution (str): Timestamp resolution (e.g. "hour", "quarterhour").
        list_timestamps_ms (int): List of timestamps in ms returned by the API.

    Returns:
        dict: A dictionary summarizing the available years, months, date range and metadata.
    """
    list_timestamps_datetime_utc = [
        ts_to_datetime(ts_ms) for ts_ms in list_timestamps_ms
    ]

    available_years = [date.year for date in list_timestamps_datetime_utc]

    year_and_available_months = {
        year: {date.month for date in list_timestamps_datetime_utc if date.year == year}
        for year in available_years
    }

    all_months = set(
        range(1, 13)
    )  # It only accepts an iterable (1,2,3,4,5,6,7,8,9,10,11,12) used to subtract to available_monts

    years_and_available_months_formatted = {
        year: "full"
        if len(available_months) == 12
        else {"missing": list(all_months - available_months)}
        for year, available_months in year_and_available_months.items()
    }

    min_date = min(list_timestamps_datetime_utc).isoformat()
    max_date = max(list_timestamps_datetime_utc).isoformat()

    d = {}
    d["filter_name"] = filter_name
    d["filter_value"] = filter_value
    d["resolution"] = resolution
    d["total_timestamps"] = len(list_timestamps_datetime_utc)
    d["data_range"] = {"min": min_date, "max": max_date}
    d["years"] = years_and_available_months_formatted
    if include_or_list:
        d["original_list_ms"] = list_timestamps_ms

    return d
