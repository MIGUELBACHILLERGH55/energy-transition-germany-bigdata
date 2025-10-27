# loader builds SourceSpec and DatasetSpec objects from the raw YAML configuration.
#
# - Example: build_source_spec(cfg, "smard") → returns a SourceSpec with all its datasets.
# - This is the only layer responsible for transforming YAML → Python objects (Specs).
# - Allows early validation before running any Extractor (fail fast if config is invalid).
#
# This module should NOT contain any extraction logic — only configuration loading/parsing.
