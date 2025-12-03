import json
from pathlib import Path


# TODO: refactor this so I can change the file_name via parameter
def save_summary_to_json(summary, output_dir: str | Path, file_name: str) -> Path:
    """Save metadata summary to JSON in the desired directory.

    Args:
        summary (dict): Well-formatted dict with indices metadata.
        output_dir: Directory where the data will be stored.

    Returns:
        str: Full path to the saved JSON file.
    """
    output_dir = Path(output_dir).resolve()

    file_path = output_dir / file_name

    output_dir.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(summary))

    return file_path
