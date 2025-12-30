from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict
from src.models.excel import ExcelReadTask


@dataclass
class PlanItem:
    """
    Represents a concrete unit of work to be executed by an extractor.

    A PlanItem is the result of the planning step (plan()), where a high-level
    dataset configuration is translated into something executable.

    Depending on the source type, a PlanItem can represent:
      - an API request over a given time window (start_ts / end_ts), or
      - the ingestion of one or more local files from an input path.

    It contains all the information needed by downstream components
    (downloader / file reader / parser) so they can remain stateless.

    In short, a PlanItem answers:
      - what dataset is being processed,
      - where the input comes from (API params or file path),
      - which logical slice of data is involved (time window, if applicable),
      - and where the output should be written (bronze/silver/gold).
    """

    source_name: str  # Logical source name (e.g. "smard", "opsd", "eea")
    dataset_name: str  # Dataset key inside the source
    dataset_id: str  # Canonical dataset identifier (for lineage / metadata)

    input_path: Path | str | None  # File or directory to read from (file-based sources)
    input_format: str
    output_path: Path  # Target path where processed data will be written

    start_ts: datetime | None = (
        None  # Start of the time window (API / time-series datasets)
    )
    end_ts: datetime | None = None  # End of the time window
    excel_tasks: list[ExcelReadTask] | None = None

    request_params: dict | None = None  # API-specific request parameters
