# src/extract/core/policies/retry.py

"""
Retry Policy
------------

Encapsulates retry behavior for transient failures.

Responsibilities:
- Define maximum retry count and backoff strategy.
- Handle retriable exceptions (network errors, timeouts, rate limits).
- Optionally provide jitter or exponential backoff.

Used by DownloaderStrategy or StorageClient to ensure resilience.
"""
