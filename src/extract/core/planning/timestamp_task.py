from dataclasses import dataclass

from .task import ExtractionTask


@dataclass
class TimestampExtractionTask(ExtractionTask):
    """
    Extraction task defined by a single timestamp in milliseconds.

    Used for APIs (like SMARD) where each request corresponds
    to an exact available timestamp.
    """

    timestamp_ms: int
