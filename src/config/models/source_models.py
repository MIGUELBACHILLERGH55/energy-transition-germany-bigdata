from typing import Dict
from dataclasses import dataclass


@dataclass
class DestinationSpec:
    path: str
    format: str | None = None
    partitioning: list[str] | None = None


@dataclass
class MetadataSpec:
    dataset_id: str
    source_resolution: str | None = None
    granularity: str | None = None
    tz: str | None = None
    schedule: str | None = None
    format: str | None = None
    description: str | None = None
    country: str | None = None
    unit: int | None = None


@dataclass
class DatasetSpec:
    name: str
    enabled: bool
    access: str
    request: Dict | None
    storage: Dict | None
    metadata: MetadataSpec | None
    destinations: Dict[str, DestinationSpec] | None
    excel: Dict | None = None


@dataclass
class SourceSpec:
    name: str
    enabled: bool
    kind: str
    availability_lag_days: int | None
    base_url: str | None
    headers: Dict | None
    retry: int | None
    timeout_s: int | None
    datasets: Dict[str, DatasetSpec]
