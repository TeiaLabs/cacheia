from datetime import datetime
from typing import Iterable
from urllib.parse import quote_plus

import httpx
from cacheia_schemas import CachedValue, DeletedResult, KeyAlreadyExists

from .exceptions import InvalidInputData

DEFAULT_URL = ""


def configure(url: str):
    global DEFAULT_URL

    DEFAULT_URL = url


def cache(instance: CachedValue) -> None:
    """
    Creates a new cache instance.
    """

    c = Client()
    c.cache(instance=instance)


def get(
    group: str | None = None,
    expires_range: tuple[float, float] | None = None,
    creation_range: tuple[datetime, datetime] | None = None,
) -> Iterable[CachedValue]:
    """
    Gets all cached values fitlering by the given parameters.
    """

    c = Client()
    return c.get(
        group=group,
        expires_range=expires_range,
        creation_range=creation_range,
    )


def get_key(key: str, allow_expired: bool = False) -> CachedValue:
    """
    Gets the cached value for the given key.
    """

    c = Client()
    return c.get_key(key=key, allow_expired=allow_expired)


def flush(
    group: str | None = None,
    expires_range: tuple[float, float] | None = None,
    creation_range: tuple[datetime, datetime] | None = None,
) -> DeletedResult:
    """'
    Flushes all keys in the cache that match the given parameters.
    """

    c = Client()
    return c.flush(
        group=group,
        expires_range=expires_range,
        creation_range=creation_range,
    )


def flush_key(key: str) -> DeletedResult:
    """
    Flushes a specific key.
    """

    c = Client()
    return c.flush_key(key=key)


class Client:
    def __init__(self, url: str | None = None) -> None:
        if url is None:
            url = DEFAULT_URL
        self._url = url.rstrip("/")

    def cache(self, instance: CachedValue) -> None:
        """
        Creates a new cache instance.
        """

        response = httpx.put(
            url=f"{self._url}/cache/",
            json=instance.model_dump(mode="json"),
        )

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
            case 409:
                raise KeyAlreadyExists(response.json())

    def get(
        self,
        group: str | None = None,
        expires_range: tuple[float, float] | None = None,
        creation_range: tuple[datetime, datetime] | None = None,
    ) -> Iterable[CachedValue]:
        """
        Gets all cached values fitlering by the given parameters.
        """

        filters = {
            "group": group,
            "expires_range": expires_range,
            "creation_range": creation_range,
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        response = httpx.get(
            url=f"{self._url}/cache/",
            params=filters,
        )

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
            case _:
                return map(lambda v: CachedValue.model_construct(**v), response.json())

    def get_key(self, key: str, allow_expired: bool = False) -> CachedValue:
        """
        Gets the cached value for the given key.
        """

        encoded_key = quote_plus(key)
        response = httpx.get(
            url=f"{self._url}/cache/{encoded_key}/",
            params={"allow_expired": allow_expired},
        )

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
            case 404:
                raise KeyError(key)
            case _:
                return CachedValue.model_construct(**response.json())

    def flush(
        self,
        group: str | None = None,
        expires_range: tuple[float, float] | None = None,
        creation_range: tuple[datetime, datetime] | None = None,
    ) -> DeletedResult:
        """
        Flushes all keys in the cache that match the given parameters.
        """

        filters = {
            "group": group,
            "expires_range": expires_range,
            "creation_range": creation_range,
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        response = httpx.delete(
            url=f"{self._url}/cache/",
            params=filters,
        )

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
            case _:
                return DeletedResult.model_construct(**response.json())

    def flush_key(self, key: str) -> DeletedResult:
        """
        Flushes a specific key.
        """

        encoded_key = quote_plus(key)
        response = httpx.delete(url=f"{self._url}/cache/{encoded_key}/")

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
            case _:
                return DeletedResult.model_construct(**response.json())

    def clear(self) -> None:
        """
        Clears the entire cache.
        """

        response = httpx.delete(url=f"{self._url}/cache/$clear/")

        match response.status_code:
            case 422:
                raise InvalidInputData(response.json())
