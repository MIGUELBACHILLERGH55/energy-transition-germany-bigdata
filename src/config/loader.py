# src/config/loader.py

import yaml
from pathlib import Path
from pprint import pprint

from .models.project_models import (
    ProjectInfo,
    StorageProfile,
    LayerDefaults,
    EnvLayerBinding,
    ProjectConfig,
)
from .models.source_models import DestinationSpec, MetadataSpec, DatasetSpec, SourceSpec

"""
Loader module
-------------

Central entrypoint for reading all YAML-based configuration.

Responsibilities:
- Load the main project configuration (project.yml).
- Load all source-specific configurations from config/sources/*.yml.
- Parse YAML dictionaries into typed dataclass objects.
- Keep the resulting ProjectConfig and SourceSpec objects available
  through a single ConfigLoader instance.
"""

PROJECT_CONFIG_PATH = Path(__file__).parent / "project.yml"
SOURCES_CONFIG_PATH = Path(__file__).parent / "sources"


class ConfigLoader:
    """
    Configuration loader for the whole project.

    On initialisation it reads:
      - project.yml → ProjectConfig
      - all files under config/sources/ → dict[name, SourceSpec]

    The idea is that the rest of the codebase can depend on this class
    instead of re-reading YAML files everywhere.
    """

    def __init__(self) -> None:
        # Load project-level configuration (storage profiles, envs, defaults, ...)
        self.project_config: ProjectConfig = self.load_project_config()
        # Load all source configurations (SMARD, AGEB, EEA, OPSD, ...)
        self.sources: dict[str, SourceSpec] = self.load_sources_config()

    def load_file(self, file_path: Path) -> dict:
        """
        Load a single YAML file and return its content as a Python dict.

        I centralise YAML loading here so that changing the loader
        (safe_load, full_load, custom loader, ...) is trivial.
        """
        with open(file_path, "r") as file:
            data = yaml.full_load(file)
        return data

    def load_project_config(self) -> ProjectConfig:
        """
        Parse project.yml into a strongly typed ProjectConfig instance.

        Steps:
        - Read the raw YAML.
        - Build ProjectInfo from the "project" block.
        - Build StorageProfile, EnvLayerBinding and LayerDefaults mappings.
        - Wrap everything into a ProjectConfig object.
        """
        data = self.load_file(PROJECT_CONFIG_PATH)

        def create_project_info(data: dict) -> ProjectInfo:
            """Extract the basic project header (name, timezone)."""
            project_info_dict = data["project"]
            return ProjectInfo(
                name=project_info_dict["name"],
                timezone=project_info_dict["timezone"],
            )

        def build_objects_from_dict(section: dict, model):
            """
            Generic helper to convert a dict-of-dicts into a dict of dataclasses.

            Example:
              profiles:
                local_fs: {type: file, base_path: "data"}
            becomes:
              {"local_fs": StorageProfile(type="file", base_path="data")}
            """
            return {key: model(**values) for key, values in section.items()}

        project_info = create_project_info(data)
        profiles = build_objects_from_dict(data["profiles"], StorageProfile)
        env_profiles = build_objects_from_dict(data["env_profiles"], EnvLayerBinding)
        defaults = build_objects_from_dict(data["defaults"], LayerDefaults)

        return ProjectConfig(
            project=project_info,
            active_env=data["active_env"],
            profiles=profiles,
            env_profiles=env_profiles,
            defaults=defaults,
        )

    def load_sources_config(self) -> dict[str, SourceSpec]:
        """
        Load and parse all source configuration files under config/sources.

        For each YAML file:
          - The top-level key is treated as the source name (e.g. "smard", "ageb").
          - The "datasets" block is converted into DatasetSpec objects.
          - Each dataset's "destinations" block becomes DestinationSpec objects.

        Returns
        -------
        dict[str, SourceSpec]
            Mapping from source name → SourceSpec.
        """

        def build_objects_from_dict(section: dict | None, model):
            """
            Helper to map a dict-of-dicts into dataclass instances.

            Returns None if the section is missing or empty.
            """
            if not section:
                return None
            return {key: model(**values) for key, values in section.items()}

        def build_datasets_from_dict(
            section: dict | None,
        ) -> dict[str, DatasetSpec] | None:
            """
            Convert the 'datasets' block into a dict of DatasetSpec objects.

            This handles:
              - optional metadata block → MetadataSpec | None
              - destinations block → dict[layer, DestinationSpec]
            """
            if not section:
                return None

            datasets: dict[str, DatasetSpec] = {}

            for dataset_name, dataset_cfg in section.items():
                metadata_dict = dataset_cfg.get("metadata", None)

                if metadata_dict:
                    # Build a typed metadata object if metadata is present.
                    metadata = MetadataSpec(**metadata_dict)
                else:
                    metadata = None

                dataset = DatasetSpec(
                    name=dataset_name,
                    enabled=dataset_cfg.get("enabled"),
                    access=dataset_cfg.get("access"),
                    request=dataset_cfg.get("request", None),
                    storage=dataset_cfg.get("storage", None),
                    metadata=metadata,
                    destinations=build_objects_from_dict(
                        dataset_cfg.get("destinations", None),
                        DestinationSpec,
                    ),
                )

                datasets[dataset_name] = dataset

            return datasets

        sources: dict[str, SourceSpec] = {}

        # Iterate over all YAML files in config/sources and build one SourceSpec per file.
        for file_path in SOURCES_CONFIG_PATH.iterdir():
            if not file_path.is_file():
                continue

            data = self.load_file(file_path)

            # Each YAML is expected to have a single top-level key: the source name.
            source_name, source_cfg = next(iter(data.items()))

            source_spec = SourceSpec(
                name=source_name,
                enabled=source_cfg.get("enabled"),
                kind=source_cfg.get("kind"),
                availability_lag_days=source_cfg.get("availability_lag_days", None),
                base_url=source_cfg.get("base_url", None),
                headers=source_cfg.get("headers", None),
                retry=source_cfg.get("retry", None),
                # Note: timeout_s could be different from retry, but for now I reuse the same key.
                timeout_s=source_cfg.get("retry", None),
                datasets=build_datasets_from_dict(source_cfg.get("datasets", None)),
            )

            sources[source_name] = source_spec

        return sources


# Singleton-style loader that can be imported from other modules.
config = ConfigLoader()
