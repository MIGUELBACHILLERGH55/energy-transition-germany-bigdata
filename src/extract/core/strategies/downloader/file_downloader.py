# src/extract/core/strategies/downloader/file_downloader.py

"""
File Downloader
---------------

Implements DownloaderStrategy for local or network-mounted files.

Responsibilities:
- Open and read files from local paths defined in the DatasetSpec.
- Support simple glob or pattern-based selection.
- Return file content as RawResponse.
- Remain lightweight and synchronous (no remote I/O).

Used mainly for ingesting static or pre-staged files.
"""
