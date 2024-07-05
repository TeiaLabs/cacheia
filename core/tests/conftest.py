import pytest
from cacheia_schemas import Backend

from cacheia import Cacheia

UNSUPPORTED = [Backend.REDIS, Backend.S3]


@pytest.fixture(scope="function", autouse=True)
def clear():
    c = Cacheia._cache
    if c is not None:
        c.clear()

    yield None

    c = Cacheia._cache
    if c is not None:
        c.clear()
