from src.extract.core.strategies.downloader_base import BaseDownloader
import requests
from dataclasses import dataclass
from src.extract.core.planning.plan_item import PlanItem
from collections import namedtuple


smard_endpoint = namedtuple(
    "Endpoint", "base_endpoint filter region resolution timestamp"
)


def build_time_series_data_endpoint(endpoint: smard_endpoint) -> str:
    """Build the time series endpoint for the URL for a SMARD API request.

    Args:
        endpoint (Endpoint): Namedtuple containing base_endpoint, filter,
        region, resolution and timestamp.

    Returns:
        str: Well-formatted API URL pointing to the time seties JSON file.
    """
    return f"{endpoint.base_endpoint}/chart_data/{endpoint.filter}/{endpoint.region}/{endpoint.filter}_{endpoint.region}_{endpoint.resolution}_{endpoint.timestamp}.json"


@dataclass
class SmardDownloader(BaseDownloader):
    def download(self, plan_item: PlanItem):
        pass
