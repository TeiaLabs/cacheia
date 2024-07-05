from typing import Literal

import pytest

from cacheia import Cacheia

Backends = Literal["mongo", "memory"]


@pytest.fixture(scope="function", autouse=True)
def clear():
    c = Cacheia._cache
    if c is not None:
        c.clear()

    yield None

    c = Cacheia._cache
    if c is not None:
        c.clear()
