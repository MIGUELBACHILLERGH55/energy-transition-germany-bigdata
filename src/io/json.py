from pathlib import Path
import json
from typing import Any


def write_json(data: dict[str, Any], output_dir: str | Path, file_name: str) -> Path:
    """
    Save a JSON response to disk.
    """
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / file_name
    file_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return file_path
