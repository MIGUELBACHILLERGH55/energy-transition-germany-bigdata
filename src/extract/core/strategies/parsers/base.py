# src/extract/core/strategies/parsers/base.py

"""
Parser Strategy Base
--------------------

Abstract base class for all ParserStrategy implementations.

Responsibilities:
- Define the interface for transforming RawResponse objects
  into structured ParsedBatch instances.
- Enforce a consistent contract across CSV, JSON, and Parquet parsers.
- Remain stateless — no side effects or persistence.
- Perform only parsing and validation, never enrichment.

Concrete subclasses should handle format-specific parsing only.
"""
