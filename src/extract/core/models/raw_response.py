# src/extract/core/models/raw_response.py

"""
Raw Response Model
------------------

Encapsulates the raw payload returned by a DownloaderStrategy.

Responsibilities:
- Store raw response content (bytes, text, or stream).
- Include metadata such as HTTP status, headers, or fetch timing.
- Remain format-agnostic until parsed by a ParserStrategy.

This model represents the bridge between network or file I/O
and the parsing stage of the extraction process.
"""
