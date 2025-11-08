# src/extract/core/resolvers/secrets_resolver.py

"""
Secrets Resolver
----------------

Resolves placeholders and environment variables in configuration values.

Responsibilities:
- Expand expressions like ${VAR_NAME} using environment variables.
- Optionally integrate with secret managers or .env files.
- Keep secret handling centralized and consistent.
- Return clean, expanded configuration dictionaries.

Used by ProfileResolver and Loader to substitute sensitive values
before building SourceSpecs.
"""
