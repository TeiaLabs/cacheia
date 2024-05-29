from multiprocessing import Manager
from typing import Iterable

from cacheia_schemas import (
    CachedValue,
    DeletedResult,
    Infostar,
    NewCachedValue,
    Ref,
    ValuedRef,
)
from pymongo import MongoClient as MongodbClient
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from ..exceptions import KeyAlreadyExists
from ..settings import SETS
from .interface import CacheClient


def _setup_client_info() -> tuple[Collection, Collection, dict[str, ValuedRef]]:
    client = MongodbClient(SETS.DB_URI)
    db = client.get_default_database()

    ref_collection = db["cache-refs"]
    value_collection = db["cache-values"]
    manager = Manager()
    memory = manager.dict()

    if not SETS.USE_LOCAL_MEM or not SETS.PRELOAD:
        return (ref_collection, value_collection, memory)  # type: ignore

    for ref in ref_collection.find():
        memory[ref["key"]] = {"ref": ref}

    for value in value_collection.find():
        if value["key"] in memory:
            memory[value["key"]]["value"] = value

    return (ref_collection, value_collection, memory)  # type: ignore


class MongoClient(CacheClient):
    _refs, _values, _memory = _setup_client_info()

    @classmethod
    def create_cache(
        cls,
        instance: NewCachedValue,
        creator: Infostar,
    ) -> None:
        if SETS.USE_LOCAL_MEM:
            if instance.key in cls._memory:
                raise KeyAlreadyExists(instance.key)

        value = ValuedRef(
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
        dict_value = value.value.model_dump()
        dict_value["_id"] = instance.key
        try:
            cls._values.insert_one(dict_value)
        except DuplicateKeyError:
            raise KeyAlreadyExists(instance.key)

        dict_ref = value.ref.model_dump()
        dict_ref["_id"] = instance.key
        try:
            cls._refs.insert_one(dict_ref)
        except DuplicateKeyError:
            cls._values.delete_one({"_id": instance.key})
            raise KeyAlreadyExists(instance.key)

        cls._memory[instance.key] = value

    @classmethod
    def get_all(
        cls,
        expires_range: str | None,
        org_handle: str | None,
        service_handle: str | None,
    ) -> Iterable[CachedValue]:
        filter = {}
        if expires_range is not None:
            start, end = map(float, expires_range.split("..."))
            filter["expires_at"] = {
                "$or": [
                    {"expires_at": None},
                    {"expires_at": {"$gte": start, "$lte": end}},
                ]
            }
        if org_handle is not None:
            filter["created_by.org_handle"] = org_handle
        if service_handle is not None:
            filter["created_by.service_handle"] = service_handle

        for val in cls._values.find(filter):
            yield CachedValue.model_construct(**val)

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
