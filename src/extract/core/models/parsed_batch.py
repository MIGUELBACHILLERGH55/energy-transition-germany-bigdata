# src/extract/core/models/parsed_batch.py

"""
Parsed Batch Model
------------------

Represents structured and validated data ready for persistence.

Responsibilities:
- Hold cleaned records or DataFrame-like structures.
- Describe format ("csv", "json", "parquet") and optional schema.
- Contain partitioning metadata for storage layout.

This model is produced by ParserStrategy and consumed by StorageClient.
It should remain lightweight and serialization-ready.
"""
