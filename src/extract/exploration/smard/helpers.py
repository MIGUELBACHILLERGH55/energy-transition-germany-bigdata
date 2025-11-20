import requests
from typing import Any
from .constants import Endpoint, base_smard_endpoint


# TODO: add a try except to make the call to the api
def fetch_json(endpoint: str, verbose=False) -> dict[str, Any]:
    r = requests.get(endpoint)
    if verbose:
        print("STATUS:", r.status_code)
        print("URL:", r.url)
        print("HEADERS:", r.headers.get("Content-Type"))
        print("TEXT:", r.text[:500])

    data = r.json()
    return data


def build_indices_endpoint(endpoint: Endpoint) -> str:
    """Build the indices endpoint for the URL for a SMARD API request.

    Args:
        endpoint (Endpoint): Namedtuple containing base_endpoint, filter,
        region and resolution.

    Returns:
        str: Well-formatted API URL pointing to the index JSON file.
    """
    return f"{endpoint.base_endpoint}/chart_data/{endpoint.filter}/{endpoint.region}/index_{endpoint.resolution}.json"


def build_time_series_data_endpoint(endpoint: Endpoint) -> str:
    """Build the time series endpoint for the URL for a SMARD API request.

    Args:
        endpoint (Endpoint): Namedtuple containing base_endpoint, filter,
        region, resolution and timestamp.

    Returns:
        str: Well-formatted API URL pointing to the time seties JSON file.
    """
    return f"{endpoint.base_endpoint}/chart_data/{endpoint.filter}/{endpoint.region}/{endpoint.filter}_{endpoint.region}_{endpoint.resolution}_{endpoint.timestamp}.json"


def build_time_series_data_endpoint_json(endpoint: Endpoint) -> str:
    """Build the time series JSON endpoint URL for a SMARD API request.

    Args:
        endpoint (Endpoint): Namedtuple containing base_endpoint, filter,
            region and timestamp.

    Returns:
        str: Fully constructed API URL pointing to the time series JSON file
            under the ``table_data`` path.
    """
    return f"{endpoint.base_endpoint}/table_data/{endpoint.filter}/{endpoint.region}/{endpoint.filter}_{endpoint.region}_quarterhour_{endpoint.timestamp}.json"
