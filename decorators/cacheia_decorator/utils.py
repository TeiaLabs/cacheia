from typing import Any

from cacheia import Cacheia
from cacheia_schemas import Backend, CachedValue, Infostar, NewCachedValue


def _try_local_cache(
    _: Infostar,
    backend: Backend,
    key: str,
) -> CachedValue | None:
    try:
        return Cacheia.get(backend=backend, key=key)
    except KeyError:
        return None


def _set_local_cache(
    creator: Infostar,
    backend: Backend,
    key: str,
    value: Any,
    group: str,
    expires_at: float | None,
):
    new_cache = NewCachedValue(key=key, value=value, group=group, expires_at=expires_at)
    Cacheia.create_cache(creator=creator, backend=backend, instance=new_cache)


def _try_remote_cache(
    creator: Infostar,
    backend: Backend,
    key: str,
) -> CachedValue | None:
    from cacheia_client import get

    try:
        return get(creator=creator, backend=backend, key=key)
    except KeyError:
        return None


def _set_remote_cache(
    creator: Infostar,
    backend: Backend,
    key: str,
    value: Any,
    group: str,
    expires_at: float | None,
):
    from cacheia_client import cache

    new_cache = NewCachedValue(key=key, value=value, group=group, expires_at=expires_at)
    cache(creator=creator, backend=backend, instance=new_cache)


def try_cache(
    creator: Infostar,
    backend: Backend,
    key: str,
    local: bool,
) -> CachedValue | None:
    if local:
        return _try_local_cache(creator, backend, key)
    else:
        return _try_remote_cache(creator, backend, key)


def set_cache(
    creator: Infostar,
    backend: Backend,
    key: str,
    value: Any,
    group: str,
    expires_at: float | None,
    local: bool,
):
    if local:
        _set_local_cache(creator, backend, key, value, group, expires_at)
    else:
        _set_remote_cache(creator, backend, key, value, group, expires_at)
