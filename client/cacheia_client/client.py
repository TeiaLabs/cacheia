from typing import Iterable

import httpx
from cacheia import KeyAlreadyExists
from cacheia_schemas import (
    Backend,
    CachedValue,
    DeletedResult,
    Infostar,
    NewCachedValue,
)

from .exceptions import InvalidInputData

DEFAULT_URL = ""


def configure(host: str):
    global DEFAULT_URL

    DEFAULT_URL = host


def cache(
    creator: Infostar,
    instance: NewCachedValue,
    backend: Backend | None = None,
) -> None:
    """
    Creates a new cache instance in the chosen backend (e.g. redis, mongo or memory).
    """

    c = Client(creator=creator, backend=backend)
    c.cache(creator=creator, instance=instance)


def get_all(
    creator: Infostar,
    expires_range: str | None = None,
    org_handle: str | None = None,
    service_handle: str | None = None,
    backend: Backend | None = None,
) -> Iterable[CachedValue]:
    """
    Gets all cached values for the given backend and filters by the given parameters.
    """

    c = Client(creator=creator, backend=backend)
    return c.get_all(
        creator=creator,
        backend=backend,
        expires_range=expires_range,
        org_handle=org_handle,
        service_handle=service_handle,
    )


def get(
    creator: Infostar,
    key: str,
    backend: Backend | None = None,
) -> CachedValue:
    """
    Gets the cached value for the given key.
    """

    c = Client(creator=creator, backend=backend)
    return c.get(creator=creator, backend=backend, key=key)


def flush_all(
    creator: Infostar,
    expired_only: bool,
    backend: Backend | None = None,
) -> DeletedResult:
    """
    Flushes all keys in the cache.

    Optionally accepts a flag that indicates if it should only flushes expired keys.
    """

    c = Client(creator=creator, backend=backend)
    return c.flush_all(
        creator=creator,
        backend=backend,
        expired_only=expired_only,
    )


def flush_some(
    creator: Infostar,
    backend: Backend | None = None,
    expires_range: str | None = None,
    org_handle: str | None = None,
    service_handle: str | None = None,
) -> DeletedResult:
    """
    Flushes all keys in the cache that match the given parameters.
    """

    c = Client(creator=creator, backend=backend)
    return c.flush_some(
        creator=creator,
        backend=backend,
        expires_range=expires_range,
        org_handle=org_handle,
        service_handle=service_handle,
    )


def flush_key(
    creator: Infostar,
    key: str,
    backend: Backend | None = None,
) -> DeletedResult:
    """
    Flushes a specific key.
    """

    c = Client(creator=creator, backend=backend)
    return c.flush_key(
        creator=creator,
        backend=backend,
        key=key,
    )


class Client:
    def __init__(
        self,
        creator: Infostar | None,
        backend: Backend | None,
        url: str | None = None,
    ) -> None:
        self._default_creator = creator
        self._default_backend = backend
        self._url = url or DEFAULT_URL

    def cache(
        self,
        creator: Infostar,
        instance: NewCachedValue,
        backend: Backend | None = None,
    ) -> None:
        """
        Creates a new cache instance in the chosen backend (e.g. redis, mongo or memory).
        """

        response = httpx.post(
            url=f"{self._url}/cache",
            json={
                "creator": creator or self._default_creator,
                "backend": backend or self._default_backend,
                "instance": instance,
            },
        )

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
            case 409:
                raise KeyAlreadyExists(response.json())

    def get_all(
        self,
        creator: Infostar,
        expires_range: str | None = None,
        org_handle: str | None = None,
        service_handle: str | None = None,
        backend: Backend | None = None,
    ) -> Iterable[CachedValue]:
        """
        Gets all cached values for the given backend and filters by the given parameters.
        """

        response = httpx.get(
            url=f"{self._url}/cache",
            params={
                "backend": backend or self._default_backend,
                "expires_range": expires_range,
                "org_handle": org_handle,
                "service_handle": service_handle,
            },
        )

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
            case _:
                return map(lambda v: CachedValue.model_construct(**v), response.json())

    def get(
        self,
        creator: Infostar,
        key: str,
        backend: Backend | None = None,
    ) -> CachedValue:
        """
        Gets the cached value for the given key.
        """

        response = httpx.get(
            url=f"{self._url}/cache/{key}/",
            params={
                "backend": backend or self._default_backend,
            },
        )

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
            case 404:
                raise KeyError(key)
            case _:
                return CachedValue.model_construct(**response.json())

    def flush_all(
        self,
        creator: Infostar,
        expired_only: bool,
        backend: Backend | None = None,
    ) -> DeletedResult:
        """
        Flushes all keys in the cache.

        Optionally accepts a flag that indicates if it should only flushes expired keys.
        """

        response = httpx.delete(
            url=f"{self._url}/cache/all/",
            params={
                "backend": backend or self._default_backend,
                "expired_only": expired_only,
            },
        )

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
            case _:
                return DeletedResult.model_construct(**response.json())

    def flush_some(
        self,
        creator: Infostar,
        backend: Backend | None = None,
        expires_range: str | None = None,
        org_handle: str | None = None,
        service_handle: str | None = None,
    ) -> DeletedResult:
        """
        Flushes all keys in the cache that match the given parameters.
        """

        response = httpx.delete(
            url=f"{self._url}/cache/some/",
            params={
                "backend": backend or self._default_backend,
                "expires_range": expires_range,
                "org_handle": org_handle,
                "service_handle": service_handle,
            },
        )

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
            case _:
                return DeletedResult.model_construct(**response.json())

    def flush_key(
        self,
        creator: Infostar,
        key: str,
        backend: Backend | None = None,
    ) -> DeletedResult:
        """
        Flushes a specific key.
        """

        response = httpx.delete(
            url=f"{self._url}/cache/{key}/",
            params={
                "backend": backend or self._default_backend,
            },
        )

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
            case _:
                return DeletedResult.model_construct(**response.json())
