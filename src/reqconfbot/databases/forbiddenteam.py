from dataclasses import dataclass

from reqconfbot.databases import BasicGuild
from reqconfbot.databases import GuildJSONDatabase


@dataclass
class ForbiddenTeamGuild(BasicGuild):
    coordinates_channel_id: int = None


class ForbiddenTeamGuildDatabase(GuildJSONDatabase[ForbiddenTeamGuild]):
    def _parse(self, data: dict) -> ForbiddenTeamGuild:
        return ForbiddenTeamGuild(**data)

    def _getJSONFileName(self) -> str:
        return "forbidden_team"

    def _createGuildData(self, guild_id: int) -> ForbiddenTeamGuild:
        return ForbiddenTeamGuild(guild_id)
