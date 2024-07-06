from dataclasses import dataclass
from typing import ClassVar
from typing import Iterable
from typing import Optional

from reqconfbot.databases import BasicGuild
from reqconfbot.databases import GuildJSONDatabase


@dataclass
class NethexGuild(BasicGuild):
    """Настройки сервера Nethex"""

    MINECRAFT_PLAYER_NAME_PLACEHOLDER: ClassVar[str] = "NICKNAME"
    DISCORD_USER_ID_PLACEHOLDER: ClassVar[str] = "ID"

    forms_channel_id: Optional[int] = None
    """ID канала для рассмотрения форм"""
    minecraft_commands_channel_id: Optional[int] = None
    """ID канала для отправки майнкрафт команд"""
    minecraft_commands_on_player_apply: Optional[tuple[str, ...]] = None
    """Команды, которые будут отправлены"""

    def __formatCommand(self, command: str, nickname: str, user_id: int) -> str:
        """Получить команду с подставленными аргументами"""
        return command.replace(self.MINECRAFT_PLAYER_NAME_PLACEHOLDER, nickname).replace(self.DISCORD_USER_ID_PLACEHOLDER, f"{user_id}")

    def getFormattedCommands(self, nickname: str, user_id: int) -> Iterable[str]:
        return (
            self.__formatCommand(cmd, nickname, user_id)
            for cmd in self.minecraft_commands_on_player_apply
        )


class NethexJsonDatabase(GuildJSONDatabase[NethexGuild]):

    def _getJSONFileName(self) -> str:
        return "nethex"

    def _parse(self, data: dict) -> NethexGuild:
        return NethexGuild(**data)

    def _createGuildData(self, guild_id: int) -> NethexGuild:
        return NethexGuild(guild_id)
