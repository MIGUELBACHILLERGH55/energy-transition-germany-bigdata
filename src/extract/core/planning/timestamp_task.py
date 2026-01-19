from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from src.extract.core.planning.api_task import APIExtractionTask


@dataclass
class TimestampExtractionTask(APIExtractionTask):
    """
    Extraction task defined by a single timestamp (ms) that usually
    returns a block of data (e.g. a full week in SMARD).

    start_date / end_date define which subset of that block
    should be kept downstream.
    """

    timestamp_ms: int = field(kw_only=True)

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    use_last_available: bool = False
