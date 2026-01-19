from dataclasses import dataclass, field
from datetime import datetime
from .api_task import APIExtractionTask


@dataclass
class RangeExtractionTask(APIExtractionTask):
    """
    Extraction task defined by a time window.

    Typical for API-based datasets queried by start/end timestamps.
    """

    start_ts: datetime = field(kw_only=True)
    end_ts: datetime = field(kw_only=True)
