# src/extract/core/streaming/checkpoint_manager.py

"""
Checkpoint Manager
------------------

Conceptual component responsible for tracking progress in streaming extractions.

Responsibilities:
- Maintain and persist offsets, sequence numbers, or timestamps per stream.
- Support recovery and exactly-once or at-least-once delivery semantics.
- Provide an interface for reading and writing checkpoints.
- Remain backend-agnostic — actual persistence (FS, DB, etc.) handled by StorageClient or future extension.

Used by StreamingExtractor to ensure safe and resumable ingestion.
"""
