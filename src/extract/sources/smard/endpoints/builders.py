from datetime import datetime, timezone
from src.extract.sources.smard.models.endpoint import (
    SmardIndicesEndpoint,
    SmardTimeseriesEndpoint,
)


def build_indices_endpoint(endpoint: SmardIndicesEndpoint) -> str:
    """Build the indices endpoint for the URL for a SMARD API request.

    Args:
        endpoint (Endpoint): Namedtuple containing base_endpoint, filter,
        region and resolution.

    Returns:
        str: Well-formatted API URL pointing to the index JSON file.
    """
    return f"{endpoint.base_endpoint}/chart_data/{endpoint.filter}/{endpoint.region}/index_{endpoint.resolution}.json"


def build_time_series_data_endpoint(endpoint: SmardTimeseriesEndpoint) -> str:
    """Build the time series endpoint for the URL for a SMARD API request.

    Args:
        endpoint (Endpoint): Namedtuple containing base_endpoint, filter,
        region, resolution and timestamp.

    Returns:
        str: Well-formatted API URL pointing to the time seties JSON file.
    """
    return f"{endpoint.base_endpoint}/chart_data/{endpoint.filter}/{endpoint.region}/{endpoint.filter}_{endpoint.region}_{endpoint.resolution}_{endpoint.timestamp_ts}.json"


def build_time_series_data_endpoint_json(endpoint: SmardTimeseriesEndpoint) -> str:
    """Build the time series JSON endpoint URL for a SMARD API request.

    Args:
        endpoint (Endpoint): Namedtuple containing base_endpoint, filter,
            region and timestamp.

    Returns:
        str: Fully constructed API URL pointing to the time series JSON file
            under the ``table_data`` path.
    """
    return f"{endpoint.base_endpoint}/table_data/{endpoint.filter}/{endpoint.region}/{endpoint.filter}_{endpoint.region}_quarterhour_{endpoint.timestamp_ts}.json"


def ts_to_datetime(ts: int, timezone=timezone.utc) -> datetime:
    return datetime.fromtimestamp(ts / 1000, tz=timezone)
