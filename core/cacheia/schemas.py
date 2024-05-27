from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

Backends = Literal["redis", "mongo", "memory"]


class Ref(BaseModel):
    key: str
    group: str
    expires_at: float | None = None
    backend: Backends = "memory"
    created_by: Infostar
    created_at: datetime = Field(default_factory=datetime.now)


class CachedValue(BaseModel):
    key: str
    value: Any
