# src/extract/core/strategies/parsers/json_parser.py

"""
JSON Parser
-----------

Implements ParserStrategy for JSON-formatted data.

Responsibilities:
- Parse JSON strings or byte payloads into structured records.
- Handle nested structures and array normalization when needed.
- Return ParsedBatch with ready-to-write clean data.
- Remain format-focused — no transformation beyond parsing.

Default parser for API and streaming JSON data sources.
"""
