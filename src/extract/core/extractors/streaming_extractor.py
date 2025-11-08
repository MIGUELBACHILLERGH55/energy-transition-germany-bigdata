# src/extract/core/extractors/streaming_extractor.py

"""
Streaming Extractor
-------------------

Conceptual contract for real-time or continuous data ingestion.
Mirrors the BatchExtractor design but operates over persistent streams.

Responsibilities:
- Manage connection lifecycle to streaming brokers or sockets.
- Consume events continuously via a StreamingClient.
- Parse each event into a ParsedRecord using a ParserStrategy.
- Persist processed records through a StorageClient or sink.
- Track offsets or checkpoints via CheckpointManager.
- Handle reconnections, backoff, and graceful shutdown.

This module defines the orchestration contract only.
No actual streaming protocol logic is implemented here.
"""
