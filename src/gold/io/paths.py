from pathlib import Path
from src.config.paths import PROJECT_ROOT


def resolve_gold_dataset_path(gold_name: str) -> Path:
    """
    Resolve the root path for a gold dataset.

    Gold datasets are final analytical products and do not depend
    on DatasetSpec or source-based layout.
    """
    return PROJECT_ROOT / "data" / "gold" / gold_name
