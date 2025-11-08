# src/extract/core/strategies/downloader/ftp_downloader.py

"""
FTP Downloader
--------------

Implements DownloaderStrategy for FTP or SFTP endpoints.

Responsibilities:
- Connect to remote FTP/SFTP servers.
- Download files specified by path or pattern.
- Return file payload and metadata as RawResponse.
- Handle connection retries and authentication gracefully.

Used for ingesting files from legacy or batch-oriented FTP systems.
"""
