# src/extract/core/strategies/storage_clients/fs_client.py

"""
Filesystem Storage Client
-------------------------

Implements StorageClient for local filesystem destinations.

Responsibilities:
- Write ParsedBatch data as files (CSV, JSON, Parquet, etc.).
- Build directory structure based on partition metadata.
- Handle overwrites safely using idempotency policy.
- Ensure atomic writes and clear error reporting.

Used primarily for landing and silver layers in local environments.
"""
