# src/extract/core/factory.py

"""
Extractor Factory
-----------------

Central entry point for creating configured extractor instances.

Responsibilities:
- Select the appropriate extractor class based on SourceSpec.mode ("batch" | "stream").
- Optionally resolve specialized extractors by source_id or kind.
- Inject all required dependencies:
  - ExecutionContext
  - DownloaderStrategy
  - ParserStrategy
  - StorageClient
  - (future) StreamingClient, CheckpointManager
- Provide a single, consistent interface for building extractors.

This module performs dependency wiring only — no business logic or I/O.
"""
