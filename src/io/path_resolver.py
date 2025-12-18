from src.config.models import project_models
from src.config.paths import PROJECT_ROOT
from src.config.models.project_models import ProjectConfig
from src.config.models.source_models import DatasetSpec, SourceSpec
from src.config.loader import config
from pathlib import Path


def resolve_layer_root(project_config: ProjectConfig, layer: str):
    if layer.casefold() not in ("landing", "bronze", "silver", "gold"):
        raise ValueError(
            "Layers available are bronze, silver or gold. Please, try again."
        )

    active_env = project_config.active_env
    env_profile = getattr(project_config.env_profiles[active_env], layer)
    storage_profile = project_config.profiles.get(env_profile)
    defaults = project_config.defaults.get(layer)

    if storage_profile.type == "file":
        layer_root = PROJECT_ROOT / storage_profile.base_path / defaults.path

    elif storage_profile.type == "s3":
        layer_root = (
            f"s3://{storage_profile.bucket}/{storage_profile.base_path}/{defaults.path}"
        )
    return layer_root


def resolve_input_path(
    project_config: ProjectConfig, dataset: DatasetSpec
) -> Path | str:
    # landing/input
    root = resolve_layer_root(project_config, "landing")
    if project_config.active_env == "local":
        return root / dataset.storage["path"]
    elif project_config.active_env == "prod":
        return f"{root}{dataset.storage['path']}"


def resolve_output_path(
    project_config: ProjectConfig, dataset: DatasetSpec, layer: str
) -> Path | str:
    # bronze/silver/gold output
    if layer not in ("bronze", "silver", "gold"):
        raise ValueError("Output layer must be bronze/silver/gold")
    root = resolve_layer_root(project_config, layer)
    dest = dataset.destinations.get(layer)
    if dest is None:
        raise ValueError(f"Dataset has no destination for layer '{layer}'")
    return root / dest.path
