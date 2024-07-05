from datetime import datetime


def ts_now() -> float:
    return datetime.now().timestamp()
