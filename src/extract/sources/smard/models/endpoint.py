from typing import Optional
from dataclasses import dataclass


@dataclass
class SmardEndpoint:
    base_endpoint: str
    filter: int
    resolution: str
    region: str = "DE"


@dataclass
class SmardIndicesEndpoint(SmardEndpoint):
    pass


@dataclass
class SmardTimeseriesEndpoint(SmardEndpoint):
    timestamp_ts: Optional[str] = None
