from __future__ import annotations

import json
from typing import Final
from typing import Optional


class ServerData:
    __KEY_FORM_CHANNEL_ID: Final[str] = "form_channel_id"
    __KEY_MAIN_CHANNEL_ID: Final[str] = "main_channel_id"

    @staticmethod
    def parseServerID(__server_id: str) -> int:
        return int(__server_id)

    @classmethod
    def fromDict(cls, server_id: str, json_dict: dict[str, int | None]) -> ServerData:
        return ServerData(
            server_id=cls.parseServerID(server_id),
            form_channel_id=json_dict[cls.__KEY_FORM_CHANNEL_ID],
            main_channel_id=json_dict[cls.__KEY_MAIN_CHANNEL_ID]
        )

    def __init__(self, server_id: int, *, form_channel_id: int = None, main_channel_id: int = None) -> None:
        self.server_id: int = server_id
        self.form_channel_id: Optional[int] = form_channel_id
        self.main_channel_id: Optional[int] = main_channel_id

    def write(self) -> tuple[str, dict[str, int]]:
        return (
            self.__writeKey(),
            {
                self.__KEY_FORM_CHANNEL_ID: self.form_channel_id,
                self.__KEY_MAIN_CHANNEL_ID: self.main_channel_id
            }
        )

    def __writeKey(self) -> str:
        return f"{self.server_id}"

    def __repr__(self) -> str:
        return f"ServerData@{self.server_id} main#{self.main_channel_id}, form#{self.form_channel_id}"


class JSONBotDatabase:

    def __init__(self, __filepath: str):
        self.__file = __filepath
        self.__data: Optional[dict[int, ServerData]] = self.__load()

    def get(self, __server_id: int) -> ServerData:
        if (ret := self.__data.get(__server_id)) is not None:
            return ret

        ret = self.__data[__server_id] = ServerData(__server_id)
        return ret

    def __load(self) -> dict[int, ServerData]:
        with open(self.__file) as f:
            loaded: dict[str, dict[str, int | None]] = json.load(f)

        ret = {
            ServerData.parseServerID(key): ServerData.fromDict(key, s_dict)
            for key, s_dict in loaded.items()
        }

        return ret

    def dump(self) -> None:
        with open(self.__file, "w") as f:
            json.dump(dict(s.write() for s in self.__data.values()), f, indent=4)
