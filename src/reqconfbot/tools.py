from __future__ import annotations

from datetime import datetime
from io import StringIO
from typing import Final

TIME_FORMAT: Final[str] = "%d-%m-%Y_%H-%M-%S"


def datetimeString(dt: datetime) -> str:
    return f"{dt:{TIME_FORMAT}}"


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


class ErrorsTyper:

    def __init__(self, title: str = "**Возникли ошибки, вот пути решения:**") -> None:
        self.__string_builder = StringBuilder(title)
        self.__failed = False

    def add(self, msg: str) -> None:
        self.__failed = True
        self.__string_builder.append(f"* {msg}")

    def isFailed(self) -> bool:
        return self.__failed

    def __str__(self) -> str:
        return self.__string_builder.toString()
