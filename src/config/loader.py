# src/config/loader.py

"""
Loader module
-------------

Parses the YAML project configuration and produces fully resolved
SourceSpec objects (BatchSourceSpec or StreamingSourceSpec).

Responsibilities:
- Load and validate YAML structure.
- Apply defaults and environment profiles.
- Resolve secrets and profiles.
- Return a list of ready-to-execute SourceSpec objects.

This module performs no I/O beyond reading the configuration file.
"""
