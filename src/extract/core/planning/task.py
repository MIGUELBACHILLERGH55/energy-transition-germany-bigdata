from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any


@dataclass
class ExtractionTask:
    """
    Base class for any extraction task.

    Represents a unit of work that can be executed by an extractor.
    It is intentionally minimal and domain-agnostic.
    """

    source_name: str
    dataset_name: str
    output_path: Path
    request_params: Optional[Dict[str, Any]] = None
