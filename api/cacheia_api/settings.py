from pydantic_settings import BaseSettings, SettingsConfigDict

from cacheia import SettingsType


class Settings(BaseSettings):
    # Uvicorn config
    CACHEIA_HOST: str = "0.0.0.0"
    CACHEIA_PORT: int = 5000
    CACHEIA_RELOAD: bool = True
    CACHEIA_WORKERS: int = 1

    # Cache config
    CACHEIA_BACKEND_SETTINGS_JSON: str | None = None
    CACHEIA_BACKEND_SETTINGS: SettingsType | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


SETS = Settings()  # type: ignore
if SETS.CACHEIA_BACKEND_SETTINGS_JSON is not None:
    import json

    SETS.CACHEIA_BACKEND_SETTINGS = json.loads(SETS.CACHEIA_BACKEND_SETTINGS_JSON)
