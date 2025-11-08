# src/extract/core/specs/source_spec.py

"""
Source Specs
------------

Defines top-level configuration contracts for data sources.

Classes:
- BatchSourceSpec → batch-mode sources (API, file, FTP, DB)
- StreamingSourceSpec → future support for real-time ingestion

Responsibilities:
- Hold connection defaults, kind, and mode ("batch" | "stream").
- Reference one or more dataset specifications.
- Be fully resolved by the Loader (all defaults and profiles applied).
- Provide immutable configuration objects for ExtractorFactory.

These specs are purely declarative — they define *what* to extract,
not *how* to execute it.
"""

from .dataset_spec import BatchDatasetSpec

class BatchSourceSpec:
    """Represents a batch-mode data source."""
    # fields like: mode, kind, defaults, datasets
    pass

class StreamingSourceSpec:
    """Future: represents a streaming source (Kafka, WS, MQTT)."""
    pass
