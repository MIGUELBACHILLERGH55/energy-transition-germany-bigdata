from datetime import date


def parse_timeseries_response(
    filter_name: str,
    filter_value: int,
    resolution: str,
    run_date: str,
    response,
    start_date: date | None,
    end_date: date | None,
    mode=str,
) -> dict:
    result = {}
    result["meta"] = {}
    result["meta"]["dataset"] = filter_name
    result["meta"]["filter_id"] = filter_value
    result["meta"]["resolution"] = resolution
    result["meta"]["run_date"] = run_date
    result["meta"]["mode"] = mode

    if mode == "last_available":
        last_available = None

        for ts, value in reversed(response["series"]):
            if value is not None:
                last_available = {"timestamps_ms": ts, "value": value}
                result["data"] = [last_available]

                result["meta"]["data_date"] = date.fromtimestamp(
                    last_available["timestamps_ms"] / 1000
                ).isoformat()

                break
    elif mode == "range":
        data = response["series"]

        parsed = []
        for ts, value in data:
            if value is None:
                continue

            point_date = date.fromtimestamp(ts / 1000)

            parsed.append({"timestamps_ms": ts, "value": value})

        result["data"] = parsed

    return result
