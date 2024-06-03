from typing import Annotated, Iterable

from cacheia import Cacheia, InvalidExpireRange, KeyAlreadyExists
from cacheia_schemas import (
    Backend,
    CachedValue,
    DeletedResult,
    Infostar,
    NewCachedValue,
)
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import UJSONResponse

from .schemas import Created
from .utils import get_backend

router = APIRouter(prefix="/cache")


@router.post("/", status_code=201, tags=["Create"])
def cache(
    creator: Infostar,
    backend: Annotated[Backend, Depends(get_backend)],
    instance: NewCachedValue,
) -> Created:
    """
    Creates a new cache instance in the chosen backend (e.g. redis, mongo or memory).
    """

    try:
        Cacheia.create_cache(creator=creator, instance=instance, backend=backend)
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
def get_all(
    # _creator: Infostar,  # Future use for business logic
    backend: Annotated[Backend, Depends(get_backend)],
    expires_range: str | None = Query(None),
    org_handle: str | None = Query(None),
    service_handle: str | None = Query(None),
) -> Iterable[CachedValue]:
    """
    Gets all cached values for the given backend and filters by the given parameters.
    """

    try:
        return Cacheia.get_all(
            backend=backend,
            expires_range=expires_range,
            org_handle=org_handle,
            service_handle=service_handle,
        )
    except InvalidExpireRange as e:
        raise HTTPException(
            detail=str(e),
            status_code=422,
        )


@router.get("/{key}/", status_code=200, tags=["Read"])
def get_key(
    # _creator: Infostar,  # Future use for business logic
    backend: Annotated[Backend, Depends(get_backend)],
    key: str,
) -> CachedValue:
    """
    Gets the cached value for the given key.
    """

    try:
        return Cacheia.get(backend=backend, key=key)
    except KeyError as e:
        raise HTTPException(
            detail=f"Key '{e}' not found",
            status_code=404,
        )


@router.delete("/all/", status_code=200, tags=["Delete"])
def flush_all(
    # _creator: Infostar,
    backend: Annotated[Backend, Depends(get_backend)],
    expired_only: bool = Query(True),
) -> DeletedResult:
    """
    Flushes all keys in the cache.

    Optionally accepts a flag that indicates if it should only flushes expired keys.
    """

    return Cacheia.flush_all(backend=backend, expired_only=expired_only)


@router.delete("/some/", status_code=200, tags=["Delete"])
def flush_some(
    # _creator: Infostar,  # Future use for business logic
    backend: Annotated[Backend, Depends(get_backend)],
    expires_range: str | None = None,
    org_handle: str | None = None,
    service_handle: str | None = None,
) -> DeletedResult:
    """
    Flushes all keys in the cache that match the given parameters.
    """

    try:
        return Cacheia.flush_some(
            backend=backend,
            expires_range=expires_range,
            org_handle=org_handle,
            service_handle=service_handle,
        )
    except InvalidExpireRange as e:
        raise HTTPException(
            detail=str(e),
            status_code=422,
        )


@router.delete("/{key}/", status_code=200, tags=["Delete"])
def flush_key(
    # _creator: Infostar,  # Future use for business logic
    backend: Annotated[Backend, Depends(get_backend)],
    key: str,
) -> DeletedResult:
    """
    Flushes a specific key.
    """

    return Cacheia.flush_key(backend=backend, key=key)
