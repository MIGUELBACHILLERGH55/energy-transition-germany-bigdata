# src/extract/core/strategies/downloader/base.py

"""
Downloader Strategy Base
------------------------

Abstract base class for all DownloaderStrategy implementations.

Responsibilities:
- Define the interface for retrieving raw data from any source.
- Provide common retry and timeout handling via policies.
- Accept a PlanItem as input and return a RawResponse.
- Remain stateless — all state lives in ExecutionContext.

Concrete implementations should handle only protocol-specific logic.
"""
