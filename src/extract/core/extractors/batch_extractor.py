# src/extract/core/extractors/batch_extractor.py

"""
Batch Extractor
---------------

Defines the orchestration flow for batch-mode data extraction.
Implements the Template Method pattern: delegates logic to strategies
while maintaining a consistent execution sequence.

Responsibilities:
- Coordinate the full extraction lifecycle:
  1. prepare() → setup sessions, headers, paths
  2. plan() → determine units of work (PlanItem list)
  3. fetch() → retrieve raw data via DownloaderStrategy
  4. parse() → transform raw payload via ParserStrategy
  5. persist_landing() → write cleaned data via StorageClient
  6. report() → summarize metrics and results
- Ensure idempotent and profile-aware persistence.
- Handle error reporting and orchestration-level metrics.

This module contains no protocol-specific logic — all details are delegated
to injected strategy classes.
"""
