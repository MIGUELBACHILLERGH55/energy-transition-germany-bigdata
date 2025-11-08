# src/extract/core/context/execution_context.py

"""
Execution Context
-----------------

Holds shared runtime metadata available to all extractors and strategies.
Immutable and scoped to a single extraction run.

Responsibilities:
- Store environment-specific metadata (env, timezone, run_id, logger).
- Propagate resolved storage profiles (landing, silver, gold).
- Provide contextual information for logging and dependency injection.
- Ensure consistent execution state across all components.

This module defines no business logic — it only encapsulates contextual data.
"""
