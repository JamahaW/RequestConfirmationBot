from pathlib import Path
from typing import Callable

from discord import ApplicationContext
from discord import Attachment
from discord import Bot
from discord import Option
from discord import TextChannel
from discord.ext.commands import Cog
from discord.ext.commands import has_permissions
from discord.ext.commands import slash_command

from reqconfbot.databases.zapretniki import ZapretnikiDatabase
from reqconfbot.databases.zapretniki import ZapretnikiGuild
from reqconfbot.special.zapretniki import CoordinatesEmbed
from reqconfbot.special.zapretniki import CoordinatesEmbedField
from reqconfbot.special.zapretniki import Dimension
from reqconfbot.utils.tools import ErrorsTyper


class ZapretnikiCog(Cog):

    def __init__(self, bot: Bot, databases_folder: Path):
        self.bot = bot
        self.database = ZapretnikiDatabase(databases_folder)

    @slash_command(name="coords")
    async def sendCoords(
            self, context: ApplicationContext,
            name: Option(str, "Название позиции"),
            dimension: Option(Dimension, "Измерение"),
            x: Option(int, "Позиция X"),
            z: Option(int, "Позиция Z"),
            y: Option(int, "Позиция Y", default=None),
            rounding: Option(bool, "Округление", default=True),
            screenshot: Option(Attachment, required=False),
            send_nether_coords: Option(bool, "Отправить координаты в незере", default=False),
            nethex_y: Option(int, "позиция Y в незере", default=None)
    ):
        if (coords_channel_id := self.database.get(context.guild_id).coordinates_channel_id) is None:
            err = ErrorsTyper()
            err.add("Канал для вывода координат ещё не настроен")
            await err.respond(context)
            return

        coords_channel = context.guild.get_channel(coords_channel_id)
        coords = [CoordinatesEmbedField(dimension, (x, y, z), rounding)]

        if send_nether_coords:
            coords.append(CoordinatesEmbedField(Dimension.NETHER, (x // 8, nethex_y, z // 8), rounding))

        await coords_channel.send(embed=CoordinatesEmbed(context.user, name, dimension, coords, screenshot))
        await context.respond(f"Координаты отправлены в {coords_channel.jump_url}", ephemeral=True)

    async def __setOutputChannel(self, context: ApplicationContext, channel: TextChannel, speciality: str, setter: Callable[[ZapretnikiGuild, int], None]):
        setter(self.database.get(context.guild_id), channel.id)
        await context.respond(f"{speciality} будут отправляться в {channel.jump_url}", ephemeral=True)
        self.database.dump()

    @slash_command(name="coords_set_channel")
    @has_permissions(administrator=True)
    async def setCoordsChannel(self, context: ApplicationContext, channel: TextChannel):
        await self.__setOutputChannel(context, channel, "Координаты", ZapretnikiGuild.setCoordinatesChannelID)

    @slash_command(name="tasks_set_channel")
    @has_permissions(administrator=True)
    async def setTasksChannel(self, context: ApplicationContext, channel: TextChannel):
        await self.__setOutputChannel(context, channel, "Задания", ZapretnikiGuild.setTasksChannelID)
