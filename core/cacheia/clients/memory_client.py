from copy import copy
from datetime import datetime
from typing import Iterable

from cacheia_schemas import (
    CachedValue,
    DeletedResult,
    Infostar,
    NewCachedValue,
    Ref,
    ValuedRef,
)

from ..exceptions import KeyAlreadyExists
from ..settings import SETS
from .interface import CacheClient


def _is_expired(expires_at: float, expires_range: str):
    start, end = map(float, expires_range.split("..."))
    return end < expires_at or expires_at < start


def _match_filter(
    ref: Ref,
    org_handle: str | None,
    service_handle: str | None,
    expires_range: str | None,
) -> bool:
    if org_handle is not None:
        if ref.created_by.org_handle != org_handle:
            return False

    if service_handle is not None:
        if ref.created_by.service_handle != service_handle:
            return False

    if expires_range is not None and ref.expires_at is not None:
        if _is_expired(ref.expires_at, expires_range):
            return False

    return True


class MemoryClient(CacheClient):
    if SETS.PROC_SAFE:
        from multiprocessing import Manager

        _manager = Manager()
        _cache: dict[str, ValuedRef] = _manager.dict()  # type: ignore
    else:
        _cache: dict[str, ValuedRef] = {}

    @classmethod
    def create_cache(
        cls,
        instance: NewCachedValue,
        creator: Infostar,
    ) -> None:
        if instance.key in cls._cache:
            raise KeyAlreadyExists(instance.key)

        cls._cache[instance.key] = ValuedRef(
            ref=Ref(
                key=instance.key,
                group=instance.group,
                expires_at=instance.expires_at,
                backend=instance.backend,
                created_by=creator,
            ),
            value=CachedValue(
                key=instance.key,
                value=instance.value,
            ),
        )

    @classmethod
    def get_all(
        cls,
        expires_range: str | None,
        org_handle: str | None,
        service_handle: str | None,
    ) -> Iterable[CachedValue]:
        for val in cls._cache.values():
            is_valid = _match_filter(
                ref=val.ref,
                org_handle=org_handle,
                service_handle=service_handle,
                expires_range=expires_range,
            )
            if is_valid:
                yield val.value

    @classmethod
    def get(cls, key: str) -> CachedValue:
        data = cls._cache[key]
        ref = data.ref
        if ref.expires_at is not None:
            now = datetime.now().timestamp()
            if ref.expires_at > now:
                del cls._cache[key]
                raise KeyError(key)

        return data.value

    @classmethod
    def flush_all(
        cls,
        expired_only: bool,
    ) -> DeletedResult:
        if expired_only:
            now = datetime.now().timestamp()
            is_expired = lambda ref: ref.expires_at is not None and ref.expires_at > now
        else:
            is_expired = lambda _: True

        count = 0
        for key in copy(cls._cache.keys()):
            value = cls._cache[key]
            if is_expired(value.ref):
                count += 1
                del cls._cache[key]

        return DeletedResult(deleted_count=count)

    @classmethod
    def flush_some(
        cls,
        expires_range: str | None,
        org_handle: str | None,
        service_handle: str | None,
    ) -> DeletedResult:
        count = 0
        for key in copy(cls._cache.keys()):
            value = cls._cache[key]
            matched = _match_filter(
                ref=value.ref,
                org_handle=org_handle,
                service_handle=service_handle,
                expires_range=expires_range,
            )
            if matched:
                count += 1
                del cls._cache[key]

        return DeletedResult(deleted_count=count)

    @classmethod
    def flush_key(cls, key: str) -> DeletedResult:
        if key in cls._cache:
            del cls._cache[key]
            return DeletedResult(deleted_count=1)
        return DeletedResult(deleted_count=0)
