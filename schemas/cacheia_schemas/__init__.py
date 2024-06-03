from datetime import datetime
from enum import StrEnum, auto
from typing import Any

from pydantic import BaseModel, Field


class Backend(StrEnum):
    REDIS = auto()
    MONGO = auto()
    MEMORY = auto()


class Infostar(BaseModel):
    org_handle: str
    service_handle: str


class NewCachedValue(BaseModel):
    key: str
    value: Any
    group: str = ""
    expires_at: float | None = None
    backend: Backend = Backend.MEMORY


class Ref(BaseModel):
    key: str
    group: str
    expires_at: float | None = None
    backend: Backend = Backend.MEMORY
    created_by: Infostar
    created_at: datetime = Field(default_factory=datetime.now)


class CachedValue(BaseModel):
    key: str
    value: Any


class ValuedRef(BaseModel):
    ref: Ref
    value: CachedValue


class DeletedResult(BaseModel):
    deleted_count: int
