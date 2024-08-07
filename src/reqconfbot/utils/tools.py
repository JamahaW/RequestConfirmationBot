from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from io import StringIO
from os import PathLike
from os import getenv
from pathlib import Path
from typing import Final

from discord import ApplicationContext
from discord import Guild
from discord import Interaction
from discord import Member
from dotenv import load_dotenv

TIME_FORMAT: Final[str] = "%d-%m-%Y_%H-%M-%S"


def getMemberByID(user_id: int, guild: Guild) -> Member:
    return guild.get_member(user_id)


def datetimeNow() -> str:
    return datetimeString(datetime.now(), "%d.%m %H:%M")


def datetimeString(dt: datetime, fmt: str = TIME_FORMAT) -> str:
    return f"{dt:{fmt}}"


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

    def __init__(self, title: str = "**Возникли ошибки:**") -> None:
        self.__string_builder = StringBuilder(title)
        self.__failed = False

    def add(self, msg: str) -> None:
        self.__failed = True
        self.__string_builder.append(f"* {msg}")

    def isFailed(self) -> bool:
        return self.__failed

    def __str__(self) -> str:
        return self.__string_builder.toString()

    async def respond(self, context: ApplicationContext | Interaction):
        await context.respond(self.__str__(), ephemeral=True)


@dataclass
class Environment:
    log_folder: Path
    databases_folder: Path
    prefix: str
    token: str = field(repr=False)

    def __init__(self, env_filepath: PathLike | str) -> None:
        load_dotenv(env_filepath)
        self.log_folder = Path(getenv("LOG_FOLDER"))
        self.databases_folder = Path(getenv("JSON_DATABASES_FOLDER"))
        self.prefix = getenv("DISCORD_BOT_PREFIX")
        self.token = getenv("DISCORD_BOT_TOKEN")
