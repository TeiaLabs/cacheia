from cacheia import CachedValue, Ref
from fastapi import APIRouter, Query

from .schemas import CreateRequest, Infostar

router = APIRouter()


@router.post("/", status_code=201)
def cache(instance: CreateRequest, creator: Infostar) -> Ref:
    """
    Creates a new cache instance in the chosen backend (e.g. redis, mongo or memory).
    """
    ...


@router.get("/", status_code=200)
def get_all_cached_values(
    creator: Infostar,
    backend: Backend | None = None,
    expires_range: str | None = None,
    org_handle: str | None = None,
    service_handle: str | None = None,
) -> list[CachedValue]:
    """
    Gets all cached values for the given backend and filters by the given parameters.
    """
    ...


@router.get("/{key}/", status_code=200)
def get_cached_value(key: str, creator: Infostar) -> CachedValue:
    """
    Gets the cached value for the given key.
    """
    ...


@router.put("/all/", status_code=204)
def flush_all(
    creator: Infostar,
    only_expired: bool = Query(True),
) -> None:
    """
    Flushes all keys in the cache, removing all registers in application DB and backend store.

    Optionally accepts a flag that indicates if it should only flushes expired keys.
    """
    ...


@router.put("/keys/", status_code=200)
def flush_keys(
    creator: Infostar,
    backend: Backend | None = None,
    expires_range: str | None = None,
    org_handle: str | None = None,
    service_handle: str | None = None,
) -> None:
    pass


@router.put("/{key}/", status_code=204)
def flush_key(key: str, creator: Infostar) -> None:
    """
    Flushes a specific key, removng its register in application DB and backend store.
    """
    ...
