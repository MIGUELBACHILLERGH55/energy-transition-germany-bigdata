"""
ParsedBatch is the minimally normalized, validated data ready for landing.

Fields (suggested):
- records: list[dict] | "DataFrame"  # decoded rows (keep it generic)
- dataset_id: str                    # same as metadata.dataset_id
- window: tuple[start, end] | None   # time coverage of this batch
- rows: int                          # row count after minimal cleaning
- meta: dict | None                  # e.g., columns, dtypes, tz info
"""
