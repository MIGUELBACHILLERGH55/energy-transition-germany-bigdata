# energy-transition-germany-bigdata/src/extract/exploration/smard/smard_indices_exploration.py

import requests
from itertools import islice
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
    "hard_coal": 4969,
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
        print("Has the following timestamps available:")

        r = requests.get(endpoint)

        print()
