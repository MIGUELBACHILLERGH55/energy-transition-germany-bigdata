def parse_available_indices_response(
    filter_name: str,
    filter_value: int,
    resolution: str,
    run_date: str,
    response,
) -> dict:
    timestamps_ms = response["timestamps"]

    result = {}
    result["dataset"] = filter_name
    result["filter_id"] = filter_value
    result["resolution"] = resolution
    result["run_date"] = run_date
    result["timestamps_ms"] = timestamps_ms

    return result
