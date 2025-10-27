# PlanItem represents a single unit of work produced by plan().
# Examples: "SMARD prices for 2025-10-25", or "read local CSV X".
#
# Fields (suggested):
# - dataset: DatasetSpec            # which dataset this item belongs to
# - window: tuple[start, end] | None  # time window for the request/file
# - endpoint: str | None            # API relative path (if access=api)
# - params: dict | None             # resolved query params (if access=api)
# - file_path: str | None           # absolute/relative path (if access=file)
# - tags: dict | None               # extra labels (run_id, retries, etc.)
