# src/extract/core/strategies/parsers/csv_parser.py

"""
CSV Parser
----------

Implements ParserStrategy for CSV-formatted data.

Responsibilities:
- Parse CSV payloads from RawResponse.
- Support custom delimiters, encodings, and header options.
- Return ParsedBatch with structured records or DataFrame-like data.
- Detect malformed rows or missing headers gracefully.

Used by BatchExtractor for CSV-based datasets.
"""
