from pathlib import Path
from typing import Callable

from discord import ApplicationContext
from discord import Attachment
from discord import Bot
from discord import Embed
from discord import Option
from discord import Role
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

    async def __setOutputChannel(self, context: ApplicationContext, channel: TextChannel, speciality: str, setter: Callable[[ZapretnikiGuild, int], None]):
        setter(self.__getGuildData(context), channel.id)
        await context.respond(f"{speciality} будут отправляться в {channel.jump_url}", ephemeral=True)
        self.database.dump()

    def __getGuildData(self, context: ApplicationContext) -> ZapretnikiGuild:
        return self.database.get(context.guild_id)

    @slash_command(name="coords_set_channel")
    @has_permissions(administrator=True)
    async def setCoordsChannel(self, context: ApplicationContext, channel: TextChannel):
        await self.__setOutputChannel(context, channel, "Координаты", ZapretnikiGuild.setCoordinatesChannelID)

    @slash_command(name="tasks_setup")
    @has_permissions(administrator=True)
    async def setTasksChannel(self, context: ApplicationContext, channel: TextChannel,):
        await self.__setOutputChannel(context, channel, "Задания", ZapretnikiGuild.setTasksChannelID)

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
        data = self.__getGuildData(context)

        if data.coordinates_channel_id is None:
            await self.__sendErrorImmediately(context, "Канал для вывода координат ещё не настроен")
            return

        coords = [CoordinatesEmbedField(dimension, (x, y, z), rounding)]

        if dimension is Dimension.OVERWORLD and send_nether_coords:
            coords.append(CoordinatesEmbedField(Dimension.NETHER, (x // 8, nethex_y, z // 8), rounding))

        await self.__sendEmbedMessage(context, data.coordinates_channel_id, CoordinatesEmbed(context.user, name, dimension, coords, screenshot), 'Координаты отправлены')

    @staticmethod
    async def __sendErrorImmediately(context, message: str):
        err = ErrorsTyper()
        err.add(message)
        await err.respond(context)

    @staticmethod
    def __getChannel(context: ApplicationContext, channel_id: int) -> TextChannel:
        return context.guild.get_channel(channel_id)

    @slash_command(name="task_add")
    async def addTask(
            self,
            context: ApplicationContext,
            role: Role,
            text: str
    ):
        data = self.__getGuildData(context)

        if data.tasks_channel_id is None:
            await self.__sendErrorImmediately(context, "Канал для вывода заданий ещё не настроен")
            return

        embed = Embed(title=f"{text}", color=role.color)
        embed.add_field(name="test", value=role.mention)
        await self.__sendEmbedMessage(context, data.tasks_channel_id, embed, "Задание отправлено")

    async def __sendEmbedMessage(self, context, channel_id: int, embed, msg):
        channel = self.__getChannel(context, channel_id)
        await channel.send(embed=embed)
        await context.respond(f"{msg} {channel.jump_url}", ephemeral=True)
