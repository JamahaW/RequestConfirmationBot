from datetime import datetime
from typing import Final

TIME_FORMAT: Final[str] = "%d-%m-%Y_%H-%M-%S"


def datetimeString(dt: datetime) -> str:
    return f"{dt:{TIME_FORMAT}}"
