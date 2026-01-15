from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from .task import ExtractionTask


@dataclass
class RangeExtractionTask(ExtractionTask):
    """
    Extraction task defined by a time window.

    Typical for API-based datasets queried by start/end timestamps.
    """

    start_ts: datetime
    end_ts: datetime

    request_params: Optional[Dict] = None
