from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from datetime import datetime
from io import StringIO
from os import PathLike
from os import getenv
from os import getenv
from os import getenv
from os import getenv
from pathlib import Path
from pathlib import Path
from pathlib import Path
from pathlib import Path
from typing import Final

from discord import ApplicationContext
from dotenv import load_dotenv

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

    async def respond(self, context: ApplicationContext):
        await context.respond(self.__str__(), ephemeral=True)


@dataclass()
class Environment:
    log_folder: Path
    database_folder: Path
    prefix: str
    token: str = field(repr=False)

    def __init__(self, env_filepath: PathLike | str) -> None:
        load_dotenv(env_filepath)
        self.log_folder = Path(getenv("LOG_FOLDER"))
        self.database_folder = Path(getenv("JSON_DATABASES_FOLDER"))
        self.prefix = getenv("DISCORD_BOT_PREFIX")
        self.token = getenv("DISCORD_BOT_TOKEN")
