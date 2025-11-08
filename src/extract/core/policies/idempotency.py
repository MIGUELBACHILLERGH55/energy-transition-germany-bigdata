# src/extract/core/policies/idempotency.py

"""
Idempotency Policy
------------------

Defines how the system ensures safe, repeatable writes.

Responsibilities:
- Prevent duplicate data writes when re-running the same extraction.
- Define overwrite, append, or skip behavior per storage layer.
- Optionally use hashing or file existence checks for detection.

This module contains only policy logic — no direct I/O operations.
"""
