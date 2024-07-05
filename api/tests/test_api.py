import pytest
from fastapi.testclient import TestClient

from .utils import create, flush_all, flush_key, flush_some, get, get_all, ts_now


def test_create(client: TestClient):
    r = create(client)
    assert isinstance(r, bool), r


def test_get(client: TestClient):
    r = create(client=client, key="test1", value="test1", expires_at=ts_now() - 10)
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = create(client=client, key="test2", value="test2")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = get_all(client=client)
    if isinstance(r, str):
        assert False, r

    values = list(r)
    assert len(values) == 1, f"Expected 1 value, got {len(values)}"
    assert values[0].key == "test2"
    assert values[0].value == "test2"


def test_get_key(client: TestClient):
    r = create(client=client, key="test", value="test")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = get(client=client, key="test")
    if isinstance(r, str):
        assert False, r

    assert r.key == "test"
    assert r.value == "test"

    r = create(client=client, key="test2", expires_at=ts_now() - 10)
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    with pytest.raises(Exception):
        get(client=client, key="test2")


def test_flush_all(client: TestClient):
    r = create(client=client, key="test1", value="test1")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = create(client=client, key="test2", value="test2")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = flush_all(client=client)
    assert isinstance(r, int), r
    assert r == 2, f"Expected 2, got {r}"


def test_flush_some(client: TestClient):
    r = create(client=client, key="test1", value="test1", group="A")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = create(client=client, key="test2", value="test2", group="B")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = flush_some(client=client, group="B")
    assert isinstance(r, int), r
    assert r == 1, f"Expected 1, got {r}"


def test_flush_key(client: TestClient):
    r = create(client=client, key="test1", value="test1")
    if isinstance(r, str):
        assert False, f"Test failed due to a failure during cache creation:\n{r}"

    r = flush_key(client=client, key="test1")
    assert isinstance(r, int), r
    assert r == 1, f"Expected 1, got {r}"
