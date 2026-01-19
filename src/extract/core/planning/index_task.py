from dataclasses import dataclass
from src.extract.core.planning.task import ExtractionTask


@dataclass
class IndexExtractionTask(ExtractionTask):
    """
    Extraction task for index / metadata endpoints.

    Typical for endpoints that expose available timestamps,
    catalogs, manifests or other non-time-windowed resources.
    """

    request_params: dict
