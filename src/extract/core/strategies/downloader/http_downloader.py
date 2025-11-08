# src/extract/core/strategies/downloader/http_downloader.py

"""
HTTP Downloader
---------------

Implements DownloaderStrategy for HTTP/HTTPS APIs.

Responsibilities:
- Perform GET or POST requests to API endpoints defined in DatasetSpec.
- Apply headers, query params, and authentication tokens.
- Handle retries, rate limits, and timeouts via policy injection.
- Return response payload and metadata as RawResponse.

This is the default downloader for REST-style API extractions.
"""
