def build_indices_endpoint(endpoint):
    return f"{endpoint.base_endpoint}/chart_data/{endpoint.filter}/{endpoint.region}/index_{endpoint.resolution}.json"


def build_time_series_data_endpoint(endpoint):
    return f"{endpoint.base_endpoint}/base_endpoint/{endpoint.filter}/{endpoint.region}/{endpoint.filter}_{endpoint.region}_{endpoint.resolution}_{endpoint.timestamp}"


def build_time_series_data_endpoint_json(endpoint):
    return f"{endpoint.base_endpoint}/table_data/{endpoint.filter}/{endpoint.region}/{endpoint.filter}_{endpoint.region}_quarterhour_{endpoint.timestamp}.json"
