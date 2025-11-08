# src/extract/core/policies/rate_limit.py

"""
Rate Limit Policy
-----------------

Controls request frequency to external APIs or data sources.

Responsibilities:
- Define maximum requests per second/minute.
- Implement sleep or token-bucket–like throttling logic.
- Enforce polite crawling and API compliance.

Applied by DownloaderStrategy before making network calls.
"""
