from datetime import datetime
from enum import StrEnum, auto
from typing import Any

from pydantic import BaseModel, Field


class Backend(StrEnum):
    REDIS = auto()
    MONGO = auto()
    MEMORY = auto()
    S3 = auto()


class CachedValue(BaseModel):
    key: str
    value: Any
    group: str | None = None
    expires_at: float | None = None
    created_at: datetime = Field(default_factory=datetime.now)


class DeletedResult(BaseModel):
    deleted_count: int
