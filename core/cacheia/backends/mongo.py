from datetime import datetime
from typing import Iterable

from cacheia_schemas import CachedValue, DeletedResult
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from ..exceptions import KeyAlreadyExists
from ..utils import ts_now
from .interface import CacheClient, CacheClientSettings
from .memory import MemoryCacheClient, MemoryCacheClientSettings


class MongoCacheClientSettings(CacheClientSettings):
    CACHE_DB_URI: str = "mongodb://localhost:27017"
    CACHE_DB_NAME: str = "cacheia"
    CACHE_COLLECTION: str = "values"
    CACHE_USE_LOCAL_MEM: bool = True
    CACHE_PRELOAD: bool = True


class MongoCacheClient(CacheClient):
    def __init__(self, settings: MongoCacheClientSettings) -> None:
        self._client = MongoClient(settings.CACHE_DB_URI)
        self._database = self._client[settings.CACHE_DB_NAME]
        self._coll = self._database[settings.CACHE_COLLECTION]

        if not settings.CACHE_USE_LOCAL_MEM or not settings.CACHE_PRELOAD:
            self._mem = None
            return

        self._mem = MemoryCacheClient(
            MemoryCacheClientSettings(
                CACHE_USE_MULTIPROCESSING=settings.CACHE_USE_MULTIPROCESSING
            )
        )

        if settings.CACHE_PRELOAD:
            for v in self._coll.find():
                key = v.pop("_id")
                self._mem.cache(CachedValue(**v, key=key))

    def cache(self, instance: CachedValue) -> None:
        try:
            dict_instance = instance.model_dump()
            dict_instance["_id"] = dict_instance.pop("key")
            self._coll.insert_one(dict_instance)
        except DuplicateKeyError:
            raise KeyAlreadyExists(instance.key)

        if self._mem is not None:
            self._mem.cache(instance)

    def get(
        self,
        group: str | None = None,
        expires_range: tuple[float, float] | None = None,
        creation_range: tuple[datetime, datetime] | None = None,
    ) -> Iterable[CachedValue]:
        filters = {}
        if group is not None:
            filters["group"] = group

        if creation_range is not None:
            filters["created_at"] = {
                "$gte": creation_range[0],
                "$lte": creation_range[1],
            }

        if expires_range is not None:
            filters["$or"] = [
                {"expires_at": None},
                {"expires_at": {"$gte": expires_range[0], "$lte": expires_range[1]}},
            ]
        else:
            filters["$or"] = [
                {"expires_at": None},
                {"expires_at": {"$gt": ts_now()}},
            ]

        for doc in self._coll.find(filters):
            key = doc.pop("_id")
            value = CachedValue.model_construct(key=key, **doc)
            if self._mem is not None:
                self._mem.cache(value)
            yield value

    def get_key(self, key: str, allow_expired: bool = False) -> CachedValue:
        if self._mem is not None:
            try:
                return self._mem.get_key(key, allow_expired=allow_expired)
            except KeyError as e:
                self._coll.delete_one({"_id": key})
                raise e

        now = ts_now()
        doc = self._coll.find_one({"_id": key})
        if not doc:
            raise KeyError(key)

        if not allow_expired:
            if doc["expires_at"] is not None and doc["expires_at"] <= now:
                self._coll.delete_one({"_id": key})
                raise KeyError(key)

        key = doc.pop("_id")
        value = CachedValue(key=key, **doc)
        if self._mem is not None:
            self._mem.cache(value)
        return value

    def flush(
        self,
        group: str | None = None,
        expires_range: tuple[float, float] | None = None,
        creation_range: tuple[datetime, datetime] | None = None,
    ) -> DeletedResult:
        filters = {}
        if group is not None:
            filters["group"] = group

        if creation_range is not None:
            filters["created_at"] = {
                "$gte": creation_range[0],
                "$lte": creation_range[1],
            }

        if expires_range is not None:
            filters["$or"] = [
                {"expires_at": None},
                {"expires_at": {"$gte": expires_range[0], "$lte": expires_range[1]}},
            ]
        else:
            filters["$or"] = [
                {"expires_at": None},
                {"expires_at": {"$gt": ts_now()}},
            ]

        if self._mem is not None:
            self._mem.clear()

        r = self._coll.delete_many(filters)
        return DeletedResult(deleted_count=r.deleted_count)

    def flush_key(self, key: str) -> DeletedResult:
        if self._mem is not None:
            self._mem.flush_key(key)

        r = self._coll.delete_one({"_id": key})
        return DeletedResult(deleted_count=r.deleted_count)

    def clear(self) -> None:
        if self._mem is not None:
            self._mem.clear()

        self._coll.delete_many({})
