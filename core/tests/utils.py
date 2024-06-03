from typing import Iterable

from cacheia import Cacheia
from cacheia_schemas import Backend, CachedValue, Infostar, NewCachedValue


def create(backend: Backend, **data) -> bool | str:
    info = {"key": "a", "value": "a", "group": "", **data}
    info.pop("backend", None)
    try:
        Cacheia.create_cache(
            NewCachedValue(backend=backend, **info),
            Infostar(org_handle="", service_handle=""),
        )
        return True
    except Exception as e:
        return str(e)


def get_all(backend: Backend, **kwargs) -> Iterable[CachedValue] | str:
    filters = {
        "expires_range": None,
        "org_handle": None,
        "service_handle": None,
        **kwargs,
    }
    try:
        iter = Cacheia.get_all(backend=backend, **filters)
        return iter
    except Exception as e:
        return str(e)


def get(backend: Backend, key: str) -> CachedValue:
    return Cacheia.get(backend=backend, key=key)


def flush_all(backend: Backend, expired_only: bool = False) -> int | str:
    try:
        count = Cacheia.flush_all(backend=backend, expired_only=expired_only)
        return count.deleted_count
    except Exception as e:
        return str(e)


def flush_some(backend: Backend, **kwargs) -> int | str:
    filters = {
        "org_handle": None,
        "service_handle": None,
        "expires_range": None,
        **kwargs,
    }
    try:
        count = Cacheia.flush_some(backend=backend, **filters)
        return count.deleted_count
    except Exception as e:
        return str(e)


def flush_key(backend: Backend, key: str) -> int | str:
    try:
        count = Cacheia.flush_key(backend=backend, key=key)
        return count.deleted_count
    except Exception as e:
        return str(e)
