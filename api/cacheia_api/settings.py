from pydantic_settings import BaseSettings, SettingsConfigDict

from cacheia import SettingsType


class Settings(BaseSettings):
    # Uvicorn config
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    RELOAD: bool = True
    WORKERS: int = 1

    # Cache config
    BACKEND_SETTINGS_JSON: str | None = None
    BACKEND_SETTINGS: SettingsType | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


SETS = Settings()  # type: ignore
if SETS.BACKEND_SETTINGS_JSON is not None:
    import json

    SETS.BACKEND_SETTINGS = json.loads(SETS.BACKEND_SETTINGS_JSON)
