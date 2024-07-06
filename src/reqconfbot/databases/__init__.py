from __future__ import annotations

import json
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Generic
from typing import TypeVar


@dataclass
class BasicGuild:
    """Общие сведения о сервере"""

    server_id: int
    """ID сервера"""

    def read(self, data: dict[str, Any]) -> BasicGuild:
        self.__dict__.update(data)
        return self

    def write(self) -> tuple[int, dict[str, Any]]:
        return int(self.server_id), self.__dict__


_T = TypeVar("_T", bound=BasicGuild)


class GuildJSONDatabase(ABC, Generic[_T]):

    def __init__(self, json_filepath: Path) -> None:
        self.__filepath = json_filepath / f"{self._getJSONFileName()}.json"
        self.__data = dict[int, _T]()
        self.__read()

    def get(self, guild_id: int) -> _T:
        """Получить данные дискорд сервера по его ID"""
        if (ret := self.__data.get(guild_id)) is None:
            ret = self.__data[guild_id] = self._createGuildData(guild_id)

        return ret

    def dump(self) -> None:
        """Сохранить значения базы"""
        with open(self.__filepath, "w") as f:
            json.dump(dict((d.write() for d in self.__data.values())), f, indent=2)

    def __read(self) -> None:
        if not self.__filepath.exists():
            return

        with open(self.__filepath, "r") as f:
            raw_data = json.load(f)

        self.__data = {int(key): self._parse(data) for key, data in raw_data.items()}

    @abstractmethod
    def _createGuildData(self, guild_id: int) -> _T:
        """Получить новый экземпляр дата класса"""

    @abstractmethod
    def _parse(self, data: dict) -> _T:
        """Преобразовать JSON словарь в дату класс"""

    @abstractmethod
    def _getJSONFileName(self) -> str:
        """Получить название JSON файла базы данных"""
