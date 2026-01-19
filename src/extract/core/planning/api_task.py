# src/extract/core/planning/api_task.py
from dataclasses import dataclass
from typing import Dict, Optional
from .task import ExtractionTask


@dataclass
class APIExtractionTask(ExtractionTask):
    """
    Base task for API-based extractions.

    Encapsulates request-level parameters required to build
    an API call (filters, resolution, query params, etc.).
    """

    request_params: Optional[Dict] = None
