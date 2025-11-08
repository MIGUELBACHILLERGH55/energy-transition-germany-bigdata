# src/extract/core/strategies/downloader/db_downloader.py

"""
Database Downloader
-------------------

Implements DownloaderStrategy for database sources.

Responsibilities:
- Connect to a database using DSN or profile parameters.
- Execute SQL queries defined in the DatasetSpec.
- Stream or fetch results into RawResponse objects.
- Apply retry and timeout policies for resilience.

This strategy focuses solely on data retrieval — no parsing or persistence.
"""
