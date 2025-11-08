# src/extract/core/strategies/parsers/parquet_parser.py

"""
Parquet Parser
--------------

Implements ParserStrategy for Parquet-formatted data.

Responsibilities:
- Load and validate Parquet payloads into structured data frames.
- Infer schema and attach it to ParsedBatch.
- Support column projection and partition awareness.
- Ensure compatibility with StorageClient for direct persistence.

Ideal for optimized batch ingestion workflows.
"""
