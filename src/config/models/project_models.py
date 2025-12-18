from dataclasses import dataclass
from typing import Dict


@dataclass
class ProjectInfo:
    name: str
    timezone: str


@dataclass
class StorageProfile:
    # Defines a storage backend (local filesystem, S3, ...)
    # Example:
    #   local_fs → type="file", base_path="data"
    #   s3_prod  → type="s3", bucket="energiewende-prod"
    type: str
    base_path: str | None = None
    bucket: str | None = None


@dataclass
class LayerDefaults:
    # Default location + file format for each logical layer (bronze/silver/gold).
    # These values are used unless a dataset overrides them.
    profile_ref: str  # name of the profile to use (e.g. "bronze" → "local_fs")
    path: str  # relative path inside the profile
    format: str  # json / parquet / ...


@dataclass
class EnvLayerBinding:
    # For a given execution environment (e.g. "local", "prod"),
    # this object tells which storage profile is used by each layer.
    #
    # Example (from project.yml):
    #   local:
    #     landing: local_fs
    #     bronze: local_fs
    #     silver: local_fs
    #     gold: local_fs
    #
    #   prod:
    #     landing: s3_prod
    #     bronze: s3_prod
    #     silver: s3_prod
    #     gold: s3_prod
    landing: str
    bronze: str
    silver: str
    gold: str


@dataclass
class ProjectConfig:
    """
    Root configuration object for the entire project.

    It contains:
      - basic project metadata (name, timezone)
      - storage profiles (local filesystem, S3, ...)
      - environment → profile bindings for each layer
      - default settings per data layer (bronze/silver/gold)
    """

    project: ProjectInfo
    active_env: str
    profiles: Dict[str, StorageProfile]  # "local_fs", "s3_prod", ...
    env_profiles: Dict[str, EnvLayerBinding]  # "local"/"prod" → layer bindings
    defaults: Dict[str, LayerDefaults]  # "bronze"/"silver"/"gold" → defaults
