from typing import Callable, ParamSpec, TypeVar

from cacheia_schemas import CachedValue

P = ParamSpec("P")
R = TypeVar("R")
F = Callable[P, R]
BuilderFunction = Callable[P, str]


def cache(
    key_builder: BuilderFunction,
    url: str | None = None,
    group: str | None = None,
    expires_at: float | None = None,
):
    from cacheia_client import cache, configure, get_key

    if url:
        configure(url)

    def decorator(func: F) -> F:
        def wrap(*args: P.args, **kwargs: P.kwargs) -> R:  # type: ignore
            key = key_builder(*args, **kwargs)
            try:
                cached_v = get_key(key)
                return cached_v.value
            except KeyError:
                pass

            value = func(*args, **kwargs)
            cached_value = CachedValue(
                key=key,
                value=value,
                group=group,
                expires_at=expires_at,
            )
            cache(cached_value)

            return value

        return wrap

    return decorator
