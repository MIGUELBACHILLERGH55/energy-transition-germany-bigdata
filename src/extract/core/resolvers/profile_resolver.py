# src/extract/core/resolvers/profile_resolver.py

"""
Profile Resolver
----------------

Resolves logical storage profiles (landing, silver, gold) into
fully qualified physical destinations.

Responsibilities:
- Merge environment-specific profiles defined in the project YAML.
- Compute absolute paths or connection parameters per layer.
- Attach resolved defaults (path, format) to each layer.
- Remain pure — performs no I/O beyond metadata resolution.

Used by the Loader to build final SourceSpec objects.
"""
