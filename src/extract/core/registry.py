# src/extract/core/registry.py

"""
Registry module
---------------

Central registry for dynamically discovering and registering available
extractors, strategies, and policies.

Responsibilities:
- Maintain mappings between string identifiers and concrete classes.
- Allow the Factory to resolve extractor or strategy implementations at runtime.
- Support custom registration for project-specific extensions.
- Provide a single import path for dependency lookup.

This module performs no business logic — it only stores and exposes references.
"""
