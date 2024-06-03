from cacheia_schemas import Backend
from fastapi import HTTPException

from ..settings import SETS


def get_backend(backend: Backend | None = None):
    if backend is None:
        if SETS.DEFAULT_BACKEND is None:
            raise HTTPException(
                status_code=400,
                detail="No default backend set and no backend value provided.",
            )

        backend = SETS.DEFAULT_BACKEND

    return backend
