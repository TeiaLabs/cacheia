from typing import Callable, Concatenate, ParamSpec, TypeVar

from cacheia_schemas import Backend, Infostar

from .utils import set_cache, try_cache

P = ParamSpec("P")
R = TypeVar("R")
F = Callable[Concatenate[Infostar, P], R]
K = Callable[Concatenate[Infostar, P], str]


def cache(
    key_builder: K,
    local: bool = True,
    backend: Backend = Backend.MEMORY,
    group: str = "",
    expires_at: float | None = None,
):
    def decorator(func: F) -> F:
        def wrap(creator: Infostar, *args: P.args, **kwargs: P.kwargs) -> R:  # type: ignore
            key = key_builder(creator, *args, **kwargs)
            value = try_cache(creator=creator, backend=backend, key=key, local=local)
            if value is None:
                value = func(creator, *args, **kwargs)
                set_cache(
                    creator=creator,
                    backend=backend,
                    key=key,
                    value=value,
                    group=group,
                    expires_at=expires_at,
                    local=local,
                )
            else:
                value = value.value

            return value

        return wrap

    return decorator
