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
from discord.ui import View

from reqconfbot.databases.zapretniki import ZapretnikiDatabase
from reqconfbot.databases.zapretniki import ZapretnikiGuild
from reqconfbot.special.zapretniki import CoordinatesEmbed
from reqconfbot.special.zapretniki import CoordinatesEmbedField
from reqconfbot.special.zapretniki import Dimension
from reqconfbot.special.zapretniki import TaskEmbed
from reqconfbot.special.zapretniki import TaskView
from reqconfbot.utils.tools import ErrorsTyper


class ZapretnikiCog(Cog):

    def __init__(self, bot: Bot, databases_folder: Path):
        self.bot = bot
        self.database = ZapretnikiDatabase(databases_folder)

    async def __updateID(self, context: ApplicationContext, entity: TextChannel | Role, e_name: str, setter: Callable[[ZapretnikiGuild, int], None]):
        try:
            setter(self.__getGuildData(context), entity.id)
        except Exception as e:
            await self.__sendErrorImmediately(context, f"{e}")
            return

        await context.respond(f"{e_name} `{entity.name}`", ephemeral=True)
        self.database.dump()

    def __getGuildData(self, context: ApplicationContext) -> ZapretnikiGuild:
        return self.database.get(context.guild_id)

    @slash_command(name="coords_set_channel")
    @has_permissions(administrator=True)
    async def __setCoordsChannel(self, context: ApplicationContext, channel: TextChannel):
        await self.__updateID(context, channel, "Отправлять координаты", ZapretnikiGuild.setCoordinatesChannelID)

    @slash_command(name="tasks_set_channel")
    @has_permissions(administrator=True)
    async def __setTasksChannel(self, context: ApplicationContext, channel: TextChannel):
        await self.__updateID(context, channel, "Отправлять Задания", ZapretnikiGuild.setTasksChannelID)

    @slash_command(name="tasks_speciality_role_add")
    @has_permissions(administrator=True)
    async def __addSpecialityRole(self, context: ApplicationContext, role: Role):
        await self.__updateID(context, role, "Специальность добавлена", ZapretnikiGuild.addSpecialityRoleID)

    @slash_command(name="tasks_speciality_role_remove")
    @has_permissions(administrator=True)
    async def __removeSpecialityRole(self, context: ApplicationContext, role: Role):
        await self.__updateID(context, role, "Специальность удалена", ZapretnikiGuild.removeSpecialityRoleID)

    @slash_command(name="coords")
    async def __sendCoords(
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

    @slash_command(name="task")
    async def __addTask(self, context: ApplicationContext, role: Option(Role, "Для какой специализации эта задача"), text: str):
        data = self.__getGuildData(context)
        err = ErrorsTyper()

        if data.tasks_channel_id is None:
            err.add("Канал для вывода заданий ещё не настроен")

        if role.id not in data.speciality_role_ids:
            err.add(f"Роль {role.mention} не является специальностью")

        if err.isFailed():
            await err.respond(context)
            return

        await self.__sendEmbedMessage(context, data.tasks_channel_id, TaskEmbed(context.user, role, text), "Задание отправлено", TaskView())

    async def __sendEmbedMessage(self, context: ApplicationContext, channel_id: int, embed: Embed, msg: str, view: View = None):
        channel = self.__getChannel(context, channel_id)
        await channel.send(embed=embed, view=view)
        await context.respond(f"{msg} {channel.jump_url}", ephemeral=True)
