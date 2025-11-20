# /energy-transition-germany-bigdata/src/extract/exploration/smard/constants.py


from collections import namedtuple

base_endpoint = "https://www.smard.de/app"
filter = None
region = "DE"  # Country: Germany
resolution = None
timestamp = None

Endpoint = namedtuple("Endpoint", "base_endpoint filter region resolution timestamp")

base_smard_endpoint_dict = {
    "base_endpoint": base_endpoint,
    "filter": filter,
    "region": region,
    "resolution": resolution,
    "timestamp": timestamp,
}

base_smard_endpoint = Endpoint(**base_smard_endpoint_dict)


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
