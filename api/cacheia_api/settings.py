from cacheia.settings import Settings as CacheiaSettings
from cacheia_schemas import Backend


class Settings(CacheiaSettings):
    # Uvicorn config
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    RELOAD: bool = False
    WORKERS: int = 8

    # Cache config
    DEFAULT_BACKEND: Backend | None = None


SETS = Settings()  # type: ignore
