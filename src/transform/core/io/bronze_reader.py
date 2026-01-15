from pathlib import Path


def resolve_bronze_leaf_paths(base_path: Path) -> list[Path]:
    return [p for p in base_path.iterdir() if p.is_dir()]
