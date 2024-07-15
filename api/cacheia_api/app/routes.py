from datetime import datetime
from typing import Annotated, Iterable
from urllib.parse import unquote_plus

from cacheia_schemas import CacheClient, CachedValue, DeletedResult, KeyAlreadyExists
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import UJSONResponse

from cacheia import Cacheia

from ..settings import SETS
from .schemas import Created

router = APIRouter(prefix="/cache")


def get_instance() -> CacheClient:
    Cacheia.setup(SETS.CACHEIA_BACKEND_SETTINGS)
    return Cacheia.get()


@router.put("/", status_code=201, tags=["Create"])
def cache(
    cache: Annotated[CacheClient, Depends(get_instance)],
    instance: CachedValue,
) -> Created:
    """
    Creates a new cache instance.
    """

    try:
        cache.cache(instance=instance)
        return UJSONResponse(
            content={"id": instance.key},
            status_code=201,
            headers={"Location": f"/cache/{instance.key}/"},
        )  # type: ignore
    except KeyAlreadyExists as e:
        raise HTTPException(
            detail=str(e),
            status_code=409,
            headers={"Location": f"/cache/{instance.key}/"},
        )


@router.get("/", status_code=200, tags=["Read"])
def get(
    cache: Annotated[CacheClient, Depends(get_instance)],
    group: str | None = Query(None),
    expires_range: tuple[float, float] | None = Query(None),
    creation_range: tuple[datetime, datetime] | None = Query(None),
) -> Iterable[CachedValue]:
    """
    Gets all cached values that matches the given parameters.
    """

    return cache.get(
        group=group,
        expires_range=expires_range,
        creation_range=creation_range,
    )


@router.get("/{key}/", status_code=200, tags=["Read"])
def get_key(
    cache: Annotated[CacheClient, Depends(get_instance)],
    key: str,
    allow_expired: bool = Query(False),
) -> CachedValue:
    """
    Gets the cached value for the given key.
    """

    print("OOGABOOGA")
    print(key)
    decoded_key = unquote_plus(key)
    try:
        return cache.get_key(key=decoded_key, allow_expired=allow_expired)
    except KeyError as e:
        raise HTTPException(
            detail=f"Key '{e}' not found",
            status_code=404,
        )


@router.delete("/", status_code=200, tags=["Delete"])
def flush(
    cache: Annotated[CacheClient, Depends(get_instance)],
    group: str | None = None,
    expires_range: tuple[float, float] | None = None,
    creation_range: tuple[datetime, datetime] | None = None,
) -> DeletedResult:
    """
    Flushes all keys in the cache that matches the given filters.
    """

    return cache.flush(
        group=group,
        expires_range=expires_range,
        creation_range=creation_range,
    )


@router.delete("/$clear/", status_code=204, tags=["Delete"])
def clear(cache: Annotated[CacheClient, Depends(get_instance)]):
    """
    Delete all cached values.
    """

    cache.clear()


@router.delete("/{key}/", status_code=200, tags=["Delete"])
def flush_key(
    cache: Annotated[CacheClient, Depends(get_instance)],
    key: str,
) -> DeletedResult:
    """
    Flushes a specific key.
    """

    decoded_key = unquote_plus(key)
    return cache.flush_key(key=decoded_key)
