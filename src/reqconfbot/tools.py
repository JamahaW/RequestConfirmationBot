from datetime import datetime
from typing import Final
from typing import Iterable

from dotenv import load_dotenv

TIME_FORMAT: Final[str] = "%d-%m-%Y_%H-%M-%S"


def datetimeString(dt: datetime) -> str:
    return f"{dt:{TIME_FORMAT}}"


def envLoad(files: Iterable[str]):
    for file in files:
        load_dotenv(file)
