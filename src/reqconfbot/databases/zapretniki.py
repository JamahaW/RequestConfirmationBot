from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from reqconfbot.databases import BasicGuild
from reqconfbot.databases import GuildJSONDatabase


@dataclass
class ZapretnikiGuild(BasicGuild):
    coordinates_channel_id: Optional[int] = None
    tasks_channel_id: Optional[int] = None

    @staticmethod
    def setCoordinatesChannelID(self: ZapretnikiGuild, channel_id: int) -> None:
        self.coordinates_channel_id = channel_id

    @staticmethod
    def setTasksChannelID(self: ZapretnikiGuild, channel_id: int) -> None:
        self.tasks_channel_id = channel_id


class ZapretnikiDatabase(GuildJSONDatabase[ZapretnikiGuild]):
    def _parse(self, data: dict) -> ZapretnikiGuild:
        return ZapretnikiGuild(**data)

    def _getJSONFileName(self) -> str:
        return "zapretniki"

    def _createGuildData(self, guild_id: int) -> ZapretnikiGuild:
        return ZapretnikiGuild(guild_id)
