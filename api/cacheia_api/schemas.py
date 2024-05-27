from typing import Any, Literal

from pydantic import BaseModel


class CreateRequest(BaseModel):
    key: str
    value: Any
    expires_at: float | None = None
    backend: Literal["redis", "mongo", "memory"] = "memory"
