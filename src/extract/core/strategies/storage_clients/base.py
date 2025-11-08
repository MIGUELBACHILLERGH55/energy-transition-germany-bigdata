# src/extract/core/strategies/storage_clients/base.py

"""
Storage Client Base
-------------------

Abstract base class for all StorageClient implementations.

Responsibilities:
- Define the interface for persisting ParsedBatch objects
  into physical destinations (filesystem, S3, database, etc.).
- Ensure idempotency and atomic write semantics.
- Use ExecutionContext and resolved profile metadata for configuration.
- Remain protocol-agnostic — subclasses handle specific backends.

Concrete implementations must implement write_batch() or similar methods.
"""
