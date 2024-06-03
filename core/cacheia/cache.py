import itertools
import re
from typing import Iterable

from cacheia_schemas import (
    Backend,
    CachedValue,
    DeletedResult,
    Infostar,
    NewCachedValue,
)

from .clients import MemoryClient, MongoClient
from .exceptions import InvalidBackendName, InvalidExpireRange
from .utils import validate_range


class Cacheia:
    @classmethod
    def create_cache(cls, instance: NewCachedValue, creator: Infostar):
        """
        Create a new cache entry.

        :param instance: The cache entry to create.
        :param creator: The creator of the cache entry.
        :raises: KeyAlreadyExists if the key already exists.
        :raises: InvalidBackendName if the backend is not valid.
        """

        match instance.backend:
            case Backend.MEMORY:
                MemoryClient.create_cache(instance, creator)
            case Backend.MONGO:
                MongoClient.create_cache(instance, creator)
            case _:
                raise InvalidBackendName(instance.backend)

    @classmethod
    def get_all(
        cls,
        backend: Backend | None,
        expires_range: str | None,
        org_handle: str | None,
        service_handle: str | None,
    ) -> Iterable[CachedValue]:
        """
        Get all cache entries filtered by the given parameters.

        :param backend: The backend to use. If None, all backends will be used.
        :param expires_range: The range of expiration time to filter by.
        :param org_handle: The organization handle to filter by.
        :param service_handle: The service handle to filter by.
        :return: An iterable of CachedValue objects.
        :raises: InvalidExpireRange if the expires_range is not valid.
        :raises: InvalidBackendName if the backend is not valid.
        """

        validate_range(expires_range)

        match backend:
            case None:
                return itertools.chain(
                    MemoryClient.get_all(
                        expires_range=expires_range,
                        org_handle=org_handle,
                        service_handle=service_handle,
                    ),
                    MongoClient.get_all(
                        expires_range=expires_range,
                        org_handle=org_handle,
                        service_handle=service_handle,
                    ),
                )
            case Backend.MEMORY:
                return MemoryClient.get_all(
                    expires_range=expires_range,
                    org_handle=org_handle,
                    service_handle=service_handle,
                )
            case Backend.MONGO:
                return MongoClient.get_all(
                    expires_range=expires_range,
                    org_handle=org_handle,
                    service_handle=service_handle,
                )
            case _:
                raise InvalidBackendName(backend)

    @classmethod
    def get(cls, backend: Backend, key: str) -> CachedValue:
        """
        Get a cache entry by key.

        :param backend: The backend to use.
        :param key: The key of the cache entry to get.
        :return: The cache entry.
        :raises: KeyError if the key does not exist.
        :raises: InvalidBackendName if the backend is not valid.
        """

        match backend:
            case Backend.MEMORY:
                return MemoryClient.get(key)
            case Backend.MONGO:
                return MongoClient.get(key)
            case _:
                raise InvalidBackendName(backend)

    @classmethod
    def flush_all(cls, backend: Backend, expired_only: bool) -> DeletedResult:
        """
        Flush all cache entries.
        If "expired_only" is True, only expired cache entries will be flushed.

        :param backend: The backend to use.
        :param expired_only: If True, only expired cache entries will be flushed.
        :return: A DeletedResult object with the count of deleted objects.
        :raises: InvalidBackendName if the backend is not valid.
        """

        match backend:
            case Backend.MEMORY:
                return MemoryClient.flush_all(expired_only)
            case Backend.MONGO:
                return MongoClient.flush_all(expired_only)
            case _:
                raise InvalidBackendName(backend)

    @classmethod
    def flush_some(
        cls,
        backend: Backend,
        expires_range: str | None,
        org_handle: str | None,
        service_handle: str | None,
    ) -> DeletedResult:
        """
        Flush some cache entries filtered by the given parameters.

        :param backend: The backend to use.
        :param expires_range: The range of expiration time to filter by in the format <start>...<end>.
        :param org_handle: The organization handle to filter by.
        :param service_handle: The service handle to filter by.
        :return: A DeletedResult object with the count of deleted objects.
        :raises: InvalidExpireRange if the expires_range is not valid.
        :raises: InvalidBackendName if the backend is not valid.
        """

        validate_range(expires_range)

        match backend:
            case Backend.MEMORY:
                return MemoryClient.flush_some(
                    expires_range=expires_range,
                    org_handle=org_handle,
                    service_handle=service_handle,
                )
            case Backend.MONGO:
                return MongoClient.flush_some(
                    expires_range=expires_range,
                    org_handle=org_handle,
                    service_handle=service_handle,
                )
            case _:
                raise InvalidBackendName(backend)

    @classmethod
    def flush_key(cls, backend: Backend, key: str) -> DeletedResult:
        """
        Flush a cache entry by key.
        :param backend: The backend to use.
        :param key: The key of the cache entry to flush.
        :return: A DeletedResult object with the count of deleted objects.
        :raises: InvalidBackendName if the backend is not valid.
        """

        match backend:
            case Backend.MEMORY:
                return MemoryClient.flush_key(key)
            case Backend.MONGO:
                return MongoClient.flush_key(key)
            case _:
                raise InvalidBackendName(backend)
