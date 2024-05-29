from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    In-Memory cache config:
    PROC_SAFE: Defines whether or not the code should protect against cross-process usage. If set to true, it will use the Manager dict object from multiprocessing module.

    Mongo cache config:
    DB_URI: MongoDB URI with the default database already set.
    USE_LOCAL_MEM: Defines whether or not a local dict should be used to prevent network calls to MongoDB.
    PRELOAD: Defines whether or not the cache should be preloaded with all the data from MongoDB.

    > Note: MongoDB local cache will **always** be a multiprocessing Managed dict.
    > Note: If USE_LOCAL_MEM is False PRELOAD will be ignored, but the opposite is not true. If PRELOAD is false,
    users can still use the local dict, but it will be populated as data is requested.
    > Note: The local dict will be all flushed if any **bulk** flush method is performed for performance reasons.

    Redis cache config:
    TODO

    S3 cache config:
    TODO
    """

    # In-Memory cache config
    PROC_SAFE: bool = False

    # Mongo cache config
    DB_URI: str = "mongodb://localhost:27107/database"
    USE_LOCAL_MEM: bool = True
    PRELOAD: bool = True

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        extra="ignore",
    )


SETS = Settings()
