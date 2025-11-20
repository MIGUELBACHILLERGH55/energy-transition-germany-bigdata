# energy-transition-germany-bigdata/src/extract/exploration/smard/times_series/helpers.py

from pprint import pprint
from ..constants import (
    Endpoint,
    base_smard_endpoint,
)
from ..helpers import (
    build_time_series_data_endpoint,
    build_indices_endpoint,
    fetch_json,
)


def smard_time_series_exploration(
    resolutions_to_explore: list[str],
    filters_to_explore: dict[str, int],
    verbose: bool = False,
    save: bool = False,
):
    for resolution in resolutions_to_explore:
        for filter_name, filter_value in filters_to_explore.items():
            indices_endpoint = base_smard_endpoint._replace(
                filter=filter_value, resolution=resolution
            )
            endpoint = build_indices_endpoint(indices_endpoint)

            data = fetch_json(endpoint)

            list_timestamps_ms = data["timestamps"]

            for ts in list_timestamps_ms:
                time_series_enpoint_nt = base_smard_endpoint._replace(
                    filter=filter_value, resolution=resolution, timestamp=str(ts)
                )
                time_series_enpoint_str = build_time_series_data_endpoint(
                    time_series_enpoint_nt
                )
                data = fetch_json(time_series_enpoint_str)

                if verbose:
                    print(f"Exploring {filter_name}")
                    pprint(data)
