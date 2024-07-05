import pytest
from cacheia_api.app import create_app
from fastapi import FastAPI
from fastapi.testclient import TestClient

from . import utils


@pytest.fixture(scope="session", autouse=True)
def app() -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def clear(client: TestClient):
    utils.clear(client)
    yield None
    utils.clear(client)
