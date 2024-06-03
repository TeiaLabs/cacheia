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
from ..utils import ts_now
from .interface import CacheClient

REFS_COL_NAME = "cache-refs"
VALUE_COL_NAME = "cache-values"


def _lookup_agg_steps() -> list:
    return [
        {
            "$lookup": {
                "from": VALUE_COL_NAME,
                "localField": "key",
                "foreignField": "_id",
                "as": "value",
            }
        },
        {
            "$unwind": {
                "path": "$value",
                "preserveNullAndEmptyArrays": False,
            }
        },
    ]


def _flush_keys(keys: list[str]) -> int:
    count = 0

    r = MongoClient._refs.delete_many({"_id": {"$in": keys}})
    count += r.deleted_count
    MongoClient._values.delete_many({"_id": {"$in": keys}})

    return count


def _setup_client_info() -> tuple[Collection, Collection, dict[str, ValuedRef]]:
    client = MongodbClient(SETS.DB_URI)
    db = client.get_default_database()

    ref_collection = db[REFS_COL_NAME]
    value_collection = db[VALUE_COL_NAME]
    manager = Manager()
    memory = manager.dict()

    if not SETS.USE_LOCAL_MEM or not SETS.PRELOAD:
        return (ref_collection, value_collection, memory)  # type: ignore

    for ref in ref_collection.find():
        memory[ref["key"]] = {"ref": Ref.model_construct(**ref)}

    for value in value_collection.find():
        if data := memory.get(value["key"]):
            memory[value["key"]] = ValuedRef(
                ref=data["ref"],
                value=CachedValue.model_construct(**value),
            )

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
            filter["$or"] = [
                {"expires_at": None},
                {"expires_at": {"$gte": start, "$lte": end}},
            ]
        else:
            filter["$or"] = [
                {"expires_at": None},
                {"expires_at": {"$gte": ts_now()}},
            ]

        if org_handle is not None:
            filter["created_by.org_handle"] = org_handle
        if service_handle is not None:
            filter["created_by.service_handle"] = service_handle

        aggregation = [{"$match": filter}]
        aggregation.extend(_lookup_agg_steps())

        cursor = cls._refs.aggregate(aggregation)
        for val in cursor:
            key = val["key"]
            value = CachedValue.model_construct(key=key, value=val["value"]["value"])
            ref = Ref.model_construct(
                key=key,
                group=val["group"],
                expires_at=val["expires_at"],
                created_by=val["created_by"],
                created_at=val["created_at"],
            )
            cls._memory[key] = ValuedRef(ref=ref, value=value)
            yield value

    @classmethod
    def get(cls, key: str) -> CachedValue:
        now = ts_now()
        if data := cls._memory.get(key):
            ref = data.ref
            value = data.value
            if ref.expires_at and ref.expires_at < now:
                cls._memory.pop(key, None)
                raise KeyError(key)
            return value

        filter = {
            "_id": key,
            "$or": [
                {"expires_at": None},
                {"expires_at": {"$gte": now}},
            ],
        }
        data = next(cls._refs.aggregate([{"$match": filter}, *_lookup_agg_steps()]))
        if not data:
            raise KeyError(key)

        ref = Ref(**data[0]["ref"])
        value = CachedValue(**data[0]["value"])
        cls._memory[key] = ValuedRef(ref=ref, value=value)
        return value

    @classmethod
    def flush_all(
        cls,
        expired_only: bool,
    ) -> DeletedResult:
        filter = {}
        if expired_only:
            filter["$or"] = [
                {"expires_at": None},
                {"expires_at": {"$lte": ts_now()}},
            ]

        count = 0
        keys = []
        for idx, doc in enumerate(cls._refs.find(filter), start=1):
            key = doc["_id"]
            keys.append(key)
            cls._memory.pop(key, None)

            if idx % 250 == 0:
                count += _flush_keys(keys)
                keys = []

        if keys:
            count += _flush_keys(keys)

        return DeletedResult(deleted_count=count)

    @classmethod
    def flush_some(
        cls,
        expires_range: str | None,
        org_handle: str | None,
        service_handle: str | None,
    ) -> DeletedResult:
        filter = {}
        if expires_range is not None:
            start, end = map(float, expires_range.split("..."))
            filter["expires_at"] = {"$gte": start, "$lte": end}
        if org_handle is not None:
            filter["created_by.org_handle"] = org_handle
        if service_handle is not None:
            filter["created_by.service_handle"] = service_handle

        count = 0
        keys = []
        for idx, doc in enumerate(cls._refs.find(filter), start=1):
            key = doc["_id"]
            keys.append(key)
            cls._memory.pop(key, None)

            if idx % 250 == 0:
                count += _flush_keys(keys)
                keys = []

        if keys:
            count += _flush_keys(keys)

        return DeletedResult(deleted_count=count)

    @classmethod
    def flush_key(cls, key: str) -> DeletedResult:
        cls._memory.pop(key, None)
        return DeletedResult(deleted_count=_flush_keys([key]))
