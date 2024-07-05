from datetime import datetime
from typing import Iterable

from cacheia_schemas import CachedValue
from fastapi.testclient import TestClient


def ts_now() -> float:
    return datetime.now().timestamp()


def create(client: TestClient, **data) -> bool | str:
    info = {"key": "a", "value": "a", **data}
    try:
        r = client.post("/cache/", json=info)
        r.raise_for_status()
        return True
    except Exception as e:
        return str(e)


def get_all(client: TestClient) -> Iterable[CachedValue] | str:
    try:
        r = client.get("/cache/")
        r.raise_for_status()
        return map(lambda x: CachedValue(**x), r.json())
    except Exception as e:
        return str(e)


def get(client: TestClient, key: str) -> CachedValue:
    r = client.get(f"/cache/{key}/")
    r.raise_for_status()
    return CachedValue.model_construct(**r.json())


def flush_all(client: TestClient) -> int | str:
    try:
        r = client.delete("/cache/")
        r.raise_for_status()
        count = r.json()
        return count["deleted_count"]
    except Exception as e:
        return str(e)


def flush_some(client: TestClient, **kwargs) -> int | str:
    try:
        r = client.delete("/cache/", params=kwargs)
        r.raise_for_status()
        count = r.json()
        return count["deleted_count"]
    except Exception as e:
        return str(e)


def flush_key(client: TestClient, key: str) -> int | str:
    try:
        r = client.delete(f"/cache/{key}/")
        r.raise_for_status()
        count = r.json()
        return count["deleted_count"]
    except Exception as e:
        return str(e)


def clear(client: TestClient):
    client.delete("/cache/$clear/")
