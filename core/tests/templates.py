import pytest
from cacheia.utils import ts_now
from cacheia_schemas import Backend

from .utils import create, flush_all, flush_key, flush_some, get, get_all


def create_test_template(backend: Backend):
    r = create(backend)
    assert isinstance(r, bool), r


def get_all_test_template(backend: Backend):
    r = create(backend, key="test1", value="test1", expires_at=ts_now() - 10)
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = create(backend, key="test2", value="test2")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = get_all(backend)
    if isinstance(r, str):
        assert False, r

    values = list(r)
    assert len(values) == 1, f"Expected 1 value, got {len(values)}"
    assert values[0].key == "test2"
    assert values[0].value == "test2"


def get_test_template(backend: Backend):
    r = create(backend, key="test", value="test")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = get(backend, "test")
    if isinstance(r, str):
        assert False, r

    assert r.key == "test"
    assert r.value == "test"

    r = create(backend, key="test2", expires_at=ts_now() - 10)
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    with pytest.raises(KeyError):
        get(backend, "test2")


def flush_all_test_template(backend: Backend):
    r = create(backend, key="test1", value="test1")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = create(backend, key="test2", value="test2")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = flush_all(backend)
    assert isinstance(r, int), r
    assert r == 2, f"Expected 2, got {r}"


def flush_some_test_template(backend: Backend):
    r = create(backend, key="test1", value="test1")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    now = ts_now()
    r = create(backend, key="test2", value="test2", expires_at=now + 5000)
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = flush_some(backend, expires_range=f"{now+4999}...{now+5001}")
    assert isinstance(r, int), r
    assert r == 1, f"Expected 1, got {r}"


def flush_key_test_template(backend: Backend):
    r = create(backend, key="test1", value="test1")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = flush_key(backend, "test1")
    assert isinstance(r, int), r
    assert r == 1, f"Expected 1, got {r}"
