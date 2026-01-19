from dataclasses import dataclass, field

from .api_task import APIExtractionTask


@dataclass
class TimestampExtractionTask(APIExtractionTask):
    """
    Extraction task defined by a single timestamp in milliseconds.

    Used for APIs (like SMARD) where each request corresponds
    to an exact available timestamp.
    """

    timestamp_ms: int = field(kw_only=True)
