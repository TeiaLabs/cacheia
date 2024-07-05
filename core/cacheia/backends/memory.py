from datetime import datetime
from multiprocessing import Manager
from typing import Iterable

from cacheia_schemas import (
    CacheClient,
    CacheClientSettings,
    CachedValue,
    DeletedResult,
    KeyAlreadyExists,
)

from .utils import ts_now


class MemoryCacheClientSettings(CacheClientSettings):
    pass


class MemoryCacheClient(CacheClient):
    def __init__(self, settings: MemoryCacheClientSettings) -> None:
        if settings.CACHE_USE_MULTIPROCESSING:
            self._manager = Manager()
            self._mem: dict[str, CachedValue] = self._manager.dict()  # type: ignore - SAFETY: multiprocessing.Manager.dict implements all dict operations
        else:
            self._mem: dict[str, CachedValue] = {}

    def cache(self, instance: CachedValue) -> None:
        if instance.key in self._mem:
            raise KeyAlreadyExists(instance.key)

        self._mem[instance.key] = instance

    def get(
        self,
        group: str | None = None,
        expires_range: tuple[float, float] | None = None,
        creation_range: tuple[datetime, datetime] | None = None,
    ) -> Iterable[CachedValue]:
        date_now = datetime.now()
        timestamp_now = date_now.timestamp()
        for value in self._mem.values():
            if group is not None and value.group != group:
                continue

            if creation_range is not None:
                if not (creation_range[0] <= date_now <= creation_range[1]):
                    continue

            if value.expires_at:
                if expires_range is not None:
                    if not (expires_range[0] <= timestamp_now <= expires_range[1]):
                        continue
                elif value.expires_at <= timestamp_now:
                    continue

            yield value

    def get_key(self, key: str, allow_expired: bool = False) -> CachedValue:
        if data := self._mem.get(key):
            if allow_expired or not data.expires_at:
                return data

            if data.expires_at <= ts_now():
                self._mem.pop(key, None)
                raise KeyError(key)

            return data

        raise KeyError(key)

    def flush(
        self,
        group: str | None = None,
        expires_range: tuple[float, float] | None = None,
        creation_range: tuple[datetime, datetime] | None = None,
    ) -> DeletedResult:
        count = 0
        date_now = datetime.now()
        timestamp_now = date_now.timestamp()
        for value in list(self._mem.values()):
            if group is not None and value.group != group:
                continue

            if creation_range is not None:
                if not (creation_range[0] < date_now < creation_range[1]):
                    continue

            if value.expires_at:
                if expires_range is not None:
                    if not (expires_range[0] < timestamp_now < expires_range[1]):
                        continue
                elif value.expires_at <= timestamp_now:
                    continue

            count += 1
            del self._mem[value.key]

        return DeletedResult(deleted_count=count)

    def flush_key(self, key: str) -> DeletedResult:
        if key in self._mem:
            del self._mem[key]
            return DeletedResult(deleted_count=1)
        return DeletedResult(deleted_count=0)

    def clear(self) -> None:
        self._mem.clear()
