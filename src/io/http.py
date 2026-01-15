import requests
from typing import Any


def fetch_json(endpoint: str, verbose=False) -> dict[str, Any]:
    r = None

    try:
        r = requests.get(endpoint)
        r.raise_for_status()
    except requests.exceptions.RequestException as ex:
        print("Error:", ex)
        return {}  # salimos temprano si falló el request

    if verbose and r is not None:
        print("STATUS:", r.status_code)
        print("URL:", r.url)
        print("HEADERS:", r.headers.get("Content-Type"))
        print("TEXT:", r.text[:500])

    return r.json()
