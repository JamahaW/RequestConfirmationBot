from dataclasses import dataclass

from discord import Guild
from discord import TextChannel

from reqconfbot.databases import BasicGuild
from reqconfbot.databases import GuildJSONDatabase


@dataclass
class ForbiddenTeamGuild(BasicGuild):
    coordinates_channel_id: int = None

    def getCoordinatedChannel(self, guild: Guild) -> TextChannel:
        return guild.get_channel(self.coordinates_channel_id)


class ForbiddenTeamGuildDatabase(GuildJSONDatabase[ForbiddenTeamGuild]):
    def _parse(self, data: dict) -> ForbiddenTeamGuild:
        return ForbiddenTeamGuild(**data)

    def _getJSONFileName(self) -> str:
        return "forbidden_team"

    def _createGuildData(self, guild_id: int) -> ForbiddenTeamGuild:
        return ForbiddenTeamGuild(guild_id)
