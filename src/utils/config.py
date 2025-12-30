# ---------------------- Agnostic configuration helpers ----------------------
from pathlib import Path
import yaml


# Resolve this file’s path and go up two parent directories.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Resolve this file’s path and go up one parent directory.
SRC_DIR = Path(__file__).resolve().parents[1]

# Path to /src/config/project.yaml.
YAML_ROUTE = SRC_DIR / "config" / "project.yaml"


def load_yaml(file_path: Path):
    """Load a YAML file and return the parsed dict."""
    with file_path.open("r") as f:
        parsed_yaml = yaml.safe_load(f)
    return parsed_yaml


def load_project_yaml(file_path=YAML_ROUTE):
    """Load the project-level YAML configuration."""
    cnf = load_yaml(file_path)
    return cnf


def get_active_profile(cfg):
    """Return the name of the active profile from the config dict."""
    return cfg["active_profile"]


def resolve_path(cfg, key: str):
    """
    Resolve a *subpath* relative to data_root of the active profile.
    Do NOT call this with key='data_root' — that is the root itself.
    """
    if key == "data_root":
        raise ValueError(
            "resolve_path() is only for subpaths — not for 'data_root' itself."
        )

    active_profile = get_active_profile(cfg)

    # Get data_root for the active profile and expand '~' if present.
    root = Path(cfg["profiles"][active_profile]["paths"]["data_root"]).expanduser()

    # Get the target subpath for the given key and expand '~' if present.
    sub = Path(cfg["profiles"][active_profile]["paths"][key]).expanduser()

    # If sub is absolute, return it normalized.
    if sub.is_absolute():
        return sub.resolve()

    # If sub is relative and root is absolute, join and normalize.
    if root.is_absolute():
        return (root / sub).resolve()
    else:
        # If both are relative, anchor at PROJECT_ROOT and normalize.
        return (PROJECT_ROOT / root / sub).resolve()


def get_source(cfg, source_key):
    """Return a source entry from cfg['sources'] by key."""
    return cfg["sources"][source_key]


def get_dataset(cfg, source: str, key: str):
    """Return a dataset entry for a given source and key."""
    return cfg["sources"][source]["datasets"][key]


# ---------------------- Quick test zone ----------------------
if __name__ == "__main__":
    cfg = load_project_yaml(YAML_ROUTE)
    print(resolve_path(cfg, "silver"))
