import pytest
from cacheia import Cacheia
from cacheia_schemas import Backend

UNSUPPORTED = [Backend.REDIS]


@pytest.fixture(scope="function", autouse=True)
def clear():
    for backend in Backend:
        if backend in UNSUPPORTED:
            continue
        Cacheia.flush_all(backend=backend, expired_only=False)
