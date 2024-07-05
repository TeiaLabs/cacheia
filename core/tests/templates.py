import pytest
from cacheia.utils import ts_now

from .conftest import Backends
from .utils import create, flush_all, flush_key, flush_some, get, get_all


def create_test_template(backend: Backends, use_multi_proc: bool = False):
    r = create(backend, use_multi_proc=use_multi_proc)
    assert isinstance(r, bool), r


def get_all_test_template(backend: Backends, use_multi_proc: bool = False):
    r = create(
        backend,
        key="test1",
        value="test1",
        expires_at=ts_now() - 10,
        use_multi_proc=use_multi_proc,
    )
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = create(backend, key="test2", value="test2", use_multi_proc=use_multi_proc)
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = get_all(backend, use_multi_proc=use_multi_proc)
    if isinstance(r, str):
        assert False, r

    values = list(r)
    assert len(values) == 1, f"Expected 1 value, got {len(values)}"
    assert values[0].key == "test2"
    assert values[0].value == "test2"


def get_test_template(backend: Backends, use_multi_proc: bool = False):
    r = create(backend, key="test", value="test", use_multi_proc=use_multi_proc)
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = get(backend, "test", use_multi_proc=use_multi_proc)
    if isinstance(r, str):
        assert False, r

    assert r.key == "test"
    assert r.value == "test"

    r = create(
        backend,
        key="test2",
        expires_at=ts_now() - 10,
        use_multi_proc=use_multi_proc,
    )
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    with pytest.raises(KeyError):
        get(backend, "test2")


def flush_all_test_template(backend: Backends, use_multi_proc: bool = False):
    r = create(backend, key="test1", value="test1", use_multi_proc=use_multi_proc)
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = create(backend, key="test2", value="test2", use_multi_proc=use_multi_proc)
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = flush_all(backend, use_multi_proc=use_multi_proc)
    assert isinstance(r, int), r
    assert r == 2, f"Expected 2, got {r}"


def flush_some_test_template(backend: Backends, use_multi_proc: bool = False):
    r = create(
        backend,
        key="test1",
        value="test1",
        group="A",
        use_multi_proc=use_multi_proc,
    )
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = create(
        backend,
        key="test2",
        value="test2",
        group="B",
        use_multi_proc=use_multi_proc,
    )
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = flush_some(backend, group="B", use_multi_proc=use_multi_proc)
    assert isinstance(r, int), r
    assert r == 1, f"Expected 1, got {r}"


def flush_key_test_template(backend: Backends, use_multi_proc: bool = False):
    r = create(backend, key="test1", value="test1", use_multi_proc=use_multi_proc)
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = flush_key(backend, "test1", use_multi_proc=use_multi_proc)
    assert isinstance(r, int), r
    assert r == 1, f"Expected 1, got {r}"
