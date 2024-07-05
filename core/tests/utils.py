from datetime import datetime
from typing import Iterable

from cacheia_schemas import CachedValue

from cacheia import Cacheia

from .conftest import Backends


def create(backend: Backends, use_multi_proc: bool = False, **data) -> bool | str:
    info = {"key": "a", "value": "a", **data}
    info.pop("backend", None)
    sets = {}
    if backend == "mongo":
        sets["CACHE_DB_URI"] = "mongodb://localhost:27017/test"

    if use_multi_proc:
        sets["CACHE_USE_MULTIPROCESSING"] = True

    Cacheia.setup(sets)
    instance = Cacheia.get()
    try:
        instance.cache(CachedValue(**info))
        return True
    except Exception as e:
        return str(e)


def get_all(
    backend: Backends, use_multi_proc: bool = False, **kwargs
) -> Iterable[CachedValue] | str:
    sets = {}
    if backend == "mongo":
        sets["CACHE_DB_URI"] = "mongodb://localhost:27017/test"

    if use_multi_proc:
        sets["CACHE_USE_MULTIPROCESSING"] = True

    Cacheia.setup(sets)
    instance = Cacheia.get()
    try:
        iter = instance.get(**kwargs)
        return iter
    except Exception as e:
        return str(e)


def get(backend: Backends, key: str, use_multi_proc: bool = False) -> CachedValue:
    sets = {}
    if backend == "mongo":
        sets["CACHE_DB_URI"] = "mongodb://localhost:27017/test"

    if use_multi_proc:
        sets["CACHE_USE_MULTIPROCESSING"] = True

    Cacheia.setup(sets)
    instance = Cacheia.get()
    return instance.get_key(key)


def flush_all(
    backend: Backends, expired_only: bool = False, use_multi_proc: bool = False
) -> int | str:
    sets = {}
    if backend == "mongo":
        sets["CACHE_DB_URI"] = "mongodb://localhost:27017/test"

    if use_multi_proc:
        sets["CACHE_USE_MULTIPROCESSING"] = True

    Cacheia.setup(sets)
    instance = Cacheia.get()
    try:
        if expired_only:
            count = instance.flush()
            return count.deleted_count
        else:
            now = datetime.now()
            end = now.timestamp() * 10
            start = now.timestamp() - end
            count = instance.flush(expires_range=(start, end))
            return count.deleted_count
    except Exception as e:
        return str(e)


def flush_some(
    backend: Backends, group: str, use_multi_proc: bool = False
) -> int | str:
    sets = {}
    if backend == "mongo":
        sets["CACHE_DB_URI"] = "mongodb://localhost:27017/test"

    if use_multi_proc:
        sets["CACHE_USE_MULTIPROCESSING"] = True

    Cacheia.setup(sets)
    instance = Cacheia.get()
    try:
        count = instance.flush(group=group)
        return count.deleted_count
    except Exception as e:
        return str(e)


def flush_key(backend: Backends, key: str, use_multi_proc: bool = False) -> int | str:
    sets = {}
    if backend == "mongo":
        sets["CACHE_DB_URI"] = "mongodb://localhost:27017/test"

    if use_multi_proc:
        sets["CACHE_USE_MULTIPROCESSING"] = True

    Cacheia.setup(sets)
    instance = Cacheia.get()
    try:
        count = instance.flush_key(key)
        return count.deleted_count
    except Exception as e:
        return str(e)
