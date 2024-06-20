from __future__ import annotations

import json
from typing import Final
from typing import Optional


class ServerData:
    SERVER_ID: Final[str] = "server_id"
    FORM_CHANNEL_ID: Final[str] = "form_channel_id"
    COMMAND_SEND_CHANNEL_ID: Final[str] = "command_send_channel_id"
    MINECRAFT_COMMAND_ON_PLAYER_ADD: Final[str] = "command_on_player_add"

    MINECRAFT_COMMAND_PLAYER_PLACEHOLDER: Final[str] = "*"

    @staticmethod
    def parseServerID(__server_id: str) -> int:
        return int(__server_id)

    @classmethod
    def fromDict(cls, server_id: str, data: dict[str, int | None | str]) -> ServerData:
        return ServerData(
            server_id=cls.parseServerID(server_id),
            form_channel_id=data.get(cls.FORM_CHANNEL_ID),
            command_send_channel_id=data.get(cls.COMMAND_SEND_CHANNEL_ID),
            command_on_player_add=data.get(cls.MINECRAFT_COMMAND_ON_PLAYER_ADD)
        )

    def __init__(
            self,
            server_id: int, *,
            form_channel_id: int = None,
            command_send_channel_id: int = None,
            command_on_player_add: str = None
    ) -> None:
        self.server_id: int = server_id
        self.form_channel_id: Optional[int] = form_channel_id
        self.command_send_channel_id: Optional[int] = command_send_channel_id
        self.command_on_player_add: Optional[str] = command_on_player_add

    def write(self) -> tuple[str, dict[str, int]]:
        return (
            self.__writeKey(),
            {
                self.FORM_CHANNEL_ID: self.form_channel_id,
                self.COMMAND_SEND_CHANNEL_ID: self.command_send_channel_id,
                self.MINECRAFT_COMMAND_ON_PLAYER_ADD: self.command_on_player_add
            }
        )

    def __writeKey(self) -> str:
        return f"{self.server_id}"


class ServerJSONDatabase:

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
            json.dump(dict(s.write() for s in self.__data.values()), f, indent=2)
