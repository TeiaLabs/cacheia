import re
from datetime import datetime

from .exceptions import InvalidExpireRange

RANGE_FORMAT = re.compile(r"^(\d+)(\.\d+)?\.\.\.(\d+)(\.\d+)?$")


def ts_now() -> float:
    return datetime.now().timestamp()


def validate_range(expires_range: str | None) -> None:
    if expires_range is None:
        return

    if not re.fullmatch(RANGE_FORMAT, expires_range):
        raise InvalidExpireRange(expires_range)

    start, end = map(float, expires_range.split("..."))
    if end < start:
        raise InvalidExpireRange(expires_range)
