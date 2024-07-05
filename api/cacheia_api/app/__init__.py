from importlib.metadata import version

from fastapi import FastAPI

from .routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Cacheia",
        version=version("cacheia"),
    )
    app.include_router(router)
    return app
