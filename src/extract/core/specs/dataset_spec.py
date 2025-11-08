# src/extract/core/specs/dataset_spec.py

"""
Batch Dataset Spec
------------------

Defines the configuration contract for a single dataset
belonging to a batch source.

Responsibilities:
- Describe dataset-level extraction parameters (access, request, schedule, tz, format).
- Optionally override default destinations per layer (landing, silver, gold).
- Remain a pure configuration model — no execution or I/O logic.
- Be fully resolved by the Loader before reaching the Extractor.

This class is used within BatchSourceSpec.datasets to define
individual extraction units.
"""

class BatchDatasetSpec:
    """Defines one dataset belonging to a batch source."""
    # fields like: enabled, access, request, schedule, tz, granularity, format, destinations
    pass
