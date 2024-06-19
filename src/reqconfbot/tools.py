from __future__ import annotations

from datetime import datetime
from io import StringIO
from typing import Final
from typing import Iterable

from dotenv import load_dotenv

TIME_FORMAT: Final[str] = "%d-%m-%Y_%H-%M-%S"


def datetimeString(dt: datetime) -> str:
    return f"{dt:{TIME_FORMAT}}"


def envLoad(files: Iterable[str]):
    for file in files:
        load_dotenv(file)


class StringBuilder(StringIO):

    def __init__(self, init_value: object = None, *, separator: str = "\n") -> None:
        self.separator = separator
        super().__init__()
        self.append(init_value)

    def append(self, obj: object) -> StringBuilder:
        self.write(obj.__str__())
        self.write(self.separator)
        return self

    def toString(self) -> str:
        return self.getvalue()

    def __str__(self) -> str:
        return self.toString()
