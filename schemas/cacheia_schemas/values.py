from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CachedValue(BaseModel):
    key: str
    value: Any
    group: str | None = None
    expires_at: float | None = None
    created_at: datetime = Field(default_factory=datetime.now)


class DeletedResult(BaseModel):
    deleted_count: int
