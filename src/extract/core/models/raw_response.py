"""
RawResponse wraps the raw payload returned by fetch() before parsing.

Fields (suggested):
- content: bytes | str | IOBase   # raw body or file-like object
- status: int | str | None        # HTTP status or equivalent (if applicable)
- dataset_id: str                 # for logging/traceability
- fetched_at: datetime            # when it was retrieved
- source_name: str                # e.g., "smard"
- meta: dict | None               # headers, size, checksum, etc.
"""
