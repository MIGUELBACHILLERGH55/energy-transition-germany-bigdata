# energy-transition-germany-bigdata/src/extract/exploration/smard/smard_indices_exploration.py

import requests
from pprint import pprint
from itertools import islice
import datetime
from constants import base_smard_endpoint
from helpers import build_indices_endpoint


# -------- SMARD ---------

resolutions_to_explore = ["hour", "quarterhour"]

filters_to_explore = {
    "market_price": 4169,
    "lignite": 1223,
    "nuclear_energy": 1224,
    "wind_offshore": 1225,
    "hydroelectricity": 1226,
    "other_conventional": 1227,
    "other_renewables": 1228,
    "biomass": 4066,
    "wind_onshore": 4067,
    "photovoltaics": 4068,
    "hard_coal": 4069,
    "pumped_storage": 4070,
    "natural_gas": 4071,
}


for resolution in resolutions_to_explore:
    for filter_name, filter_value in filters_to_explore.items():
        indices_endpoint = base_smard_endpoint._replace(
            filter=filter_value, resolution=resolution
        )
        endpoint = build_indices_endpoint(indices_endpoint)

        print(
            f"------- Exporing Smard Indices Endpoint: {indices_endpoint.base_endpoint} -------"
        )
        print(
            f"{filter_name.capitalize()} with resolution: {indices_endpoint.resolution}"
        )
        print("Preview of the timestamps available:")

        r = requests.get(endpoint)
        data = r.json()
        timestamps = data["timestamps"]

        indices_curent_cfg = {}
        # Since ts are written in ms we will store both the ms and the translated date to show the user:
        for ts in timestamps:
            ts_ms = str(ts) + "ms"
            ts_dt_str = datetime.datetime.fromtimestamp(ts / 1000).isoformat()

            indices_curent_cfg[ts_ms] = ts_dt_str

        pprint(list(indices_curent_cfg.items())[:20])

        # TODO:
        # 1) Build a temporal summary for each (filter, resolution):
        #    - min/max timestamp, total count
        #    - available years and months per year
        # 2) Create a helper to compute this summary from the raw timestamps.
        # 3) Create another helper to save the summary as JSON.
        # 4) (Optional) Save the full timestamp→date mapping in a separate JSON file.
        #
        # Data structure for the summary:
        # {
        #     "filter_name": "...",
        #     "filter_value": ...,
        #     "resolution": "...",
        #     "total_timestamps": ...,
        #     "date_range": {
        #         "min": "...",
        #         "max": "..."
        #     },
        #     "years": {
        #         "2020": ["01", "02", "03", ...],
        #         "2021": ["05", "06", ...],
        #         ...
        #     }
        # }

        print()
