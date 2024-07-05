from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from cacheia_schemas import CachedValue, DeletedResult
from pydantic_settings import BaseSettings, SettingsConfigDict


class CacheClientSettings(BaseSettings):
    CACHE_USE_MULTIPROCESSING: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class CacheClient(ABC):
    @abstractmethod
    def __init__(self, settings: CacheClientSettings) -> None: ...

    @abstractmethod
    def cache(self, instance: CachedValue) -> None:
        """
        Cache a value.

        :param instance: CachedValue instance
        :raises KeyAlreadyExists: if key already exists in cache
        """
        ...

    @abstractmethod
    def get(
        self,
        group: str | None = None,
        expires_range: tuple[float, float] | None = None,
        creation_range: tuple[datetime, datetime] | None = None,
    ) -> Iterable[CachedValue]:
        """
        Get all values that matches given filters.

        :param expires_range: (start, end) range of expiration time, if empty
        defaults to all non-expired values (e.g. 'expires_at' greater than now).
        :param creation_range: (start, end) range of creation time.
        :param group: group name
        :return: an iterable of CachedValue objects
        """
        ...

    @abstractmethod
    def get_key(self, key: str, allow_expired: bool = False) -> CachedValue:
        """
        Get a value by key if found in cache.

        If 'allow_expired' is True and the value is expired, it will be returned anyway.
        Otherwise it will be removed from the cache and raise KeyError.

        :param key: key to search for
        :param allow_expired: if True, expired values will be returned anyway
        :return: instance of CachedValue object
        :raises KeyError: if key does not exist or is expired
        """
        ...

    @abstractmethod
    def flush(
        self,
        group: str | None = None,
        expires_range: tuple[float, float] | None = None,
        creation_range: tuple[datetime, datetime] | None = None,
    ) -> DeletedResult:
        """
        Flush all values that matches given filters.

        :param expires_range: (start, end) range of expiration time, if empty
        defaults to all non-expired values (e.g. 'expires_at' greater than now).
        > Note: 'start' and 'end' are exclusive.
        :param creation_range: (start, end) range of creation time.
        > Note: 'start' and 'end' are exclusive.
        :param group: group name
        :return: DeletedResult object
        """
        ...

    @abstractmethod
    def flush_key(self, key: str) -> DeletedResult:
        """
        Delete a key from cache if found.
        """
        ...

    @abstractmethod
    def clear(self) -> None:
        """
        Delete all cached values.

        For performance reasons, this method is preferred over 'flush'
        for a full cleanup to by pass any filters and delete all values.
        """
        ...
