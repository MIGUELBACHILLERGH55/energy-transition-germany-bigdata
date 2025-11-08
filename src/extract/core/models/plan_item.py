# src/extract/core/models/plan_item.py

"""
Plan Item Model
---------------

Represents a single planned extraction unit before any I/O occurs.

Responsibilities:
- Define what needs to be fetched (dataset, partition, request parameters).
- Contain metadata for partitioning or time ranges.
- Provide a deterministic relative output path for persistence.

This model is produced by Extractor.plan() and consumed by Extractor.fetch().
It carries only logical information — no data payloads.
"""
