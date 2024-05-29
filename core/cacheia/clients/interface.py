from abc import ABC, abstractmethod
from typing import Iterable

from cacheia_schemas import CachedValue, DeletedResult, Infostar, NewCachedValue


class CacheClient(ABC):
    @classmethod
    @abstractmethod
    def create_cache(
        cls,
        instance: NewCachedValue,
        creator: Infostar,
    ):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_all(
        cls,
        expires_range: str | None,
        org_handle: str | None,
        service_handle: str | None,
    ) -> Iterable[CachedValue]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get(cls, key: str) -> CachedValue:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def flush_all(cls, expired_only: bool) -> DeletedResult:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def flush_some(
        cls,
        expires_range: str | None,
        org_handle: str | None,
        service_handle: str | None,
    ) -> DeletedResult:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def flush_key(cls, key: str) -> DeletedResult:
        raise NotImplementedError()
