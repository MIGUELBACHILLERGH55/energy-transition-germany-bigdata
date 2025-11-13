from collections import namedtuple

base_endpoint = "https://www.smard.de/app/"
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
