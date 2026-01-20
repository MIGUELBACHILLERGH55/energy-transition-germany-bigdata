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
                )

                break
    elif mode == "range":
        # To do
        data = response["series"]
        ts_list = [item[0] for item in data]

        date_list = [date.fromtimestamp(ts / 1000) for ts in ts_list]

        index_list = []
        for index, date_rg in enumerate(date_list):
            if start_date <= date_rg <= end_date:
                index_list.append(index)

        selected_data = data[index_list[0] :: index_list[-1]]

        data = [{"timestamps_ms": item[0], "value": item[1]} for item in selected_data]

        result["data"] = data

    return result
