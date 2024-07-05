from typing import Callable

from cacheia_schemas import CacheClient, CacheClientSettings, InvalidSettings
from pydantic import BaseModel

from .backends import (
    MemoryCacheClient,
    MemoryCacheClientSettings,
    MongoCacheClient,
    MongoCacheClientSettings,
)

CacheType = MemoryCacheClient | MongoCacheClient
SettingsType = MemoryCacheClientSettings | MongoCacheClientSettings
MappingKey = type[CacheClientSettings]


class AnySettings(BaseModel):
    settings: SettingsType


class Cacheia:
    _cache: CacheType | None = None
    _client_mapping: dict[MappingKey, Callable[[MappingKey], CacheClient]] = {
        MemoryCacheClientSettings: lambda sets: MemoryCacheClient(sets),  # type: ignore
        MongoCacheClientSettings: lambda sets: MongoCacheClient(sets),  # type: ignore
    }

    @classmethod
    def extend(cls, settings: CacheClientSettings, client: type[CacheClient]):
        cls._client_mapping[type(settings)] = lambda sets: client(sets)  # type: ignore

    @classmethod
    def setup(cls, settings: SettingsType | dict | None = None) -> None:
        if cls._cache is not None:
            return

        if settings is None:
            settings = {}

        if isinstance(settings, dict):
            any_sets = AnySettings(settings=settings)  # type: ignore
            settings = any_sets.settings

        if type(settings) not in cls._client_mapping:
            raise InvalidSettings(str(type(settings)))

        cls._cache = cls._client_mapping[type(settings)](settings)  # type: ignore

    @classmethod
    def get(cls) -> CacheClient:
        if cls._cache is None:
            m = "Cacheia is not setup yet. Please call `Cacheia.setup` before using `Cacheia.get`"
            raise RuntimeError(m)

        return cls._cache
