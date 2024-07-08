from dataclasses import dataclass

from discord import Guild
from discord import TextChannel

from reqconfbot.databases import BasicGuild
from reqconfbot.databases import GuildJSONDatabase


@dataclass
class ZapretnikiGuild(BasicGuild):
    coordinates_channel_id: int = None

    def getCoordinatedChannel(self, guild: Guild) -> TextChannel:
        return guild.get_channel(self.coordinates_channel_id)


class ZapretnikiDatabase(GuildJSONDatabase[ZapretnikiGuild]):
    def _parse(self, data: dict) -> ZapretnikiGuild:
        return ZapretnikiGuild(**data)

    def _getJSONFileName(self) -> str:
        return "zapretniki"

    def _createGuildData(self, guild_id: int) -> ZapretnikiGuild:
        return ZapretnikiGuild(guild_id)
