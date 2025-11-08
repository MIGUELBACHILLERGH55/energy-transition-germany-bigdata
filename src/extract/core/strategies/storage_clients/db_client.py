# src/extract/core/strategies/storage_clients/db_client.py

"""
Database Storage Client
-----------------------

Implements StorageClient for relational or analytical databases.

Responsibilities:
- Write ParsedBatch data into database tables.
- Support upsert, truncate-insert, or append modes.
- Use connection parameters resolved from ProfileResolver.
- Ensure transactional safety and idempotent writes.

Used for gold-layer persistence or analytical targets.
"""
