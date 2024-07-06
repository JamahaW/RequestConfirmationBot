from pathlib import Path
from typing import ClassVar
from typing import Optional

from discord import ApplicationContext
from discord import Bot
from discord import Option
from discord import TextChannel
from discord.ext.commands import Cog
from discord.ext.commands import has_permissions
from discord.ext.commands import slash_command

from reqconfbot.databases.nethex import NethexGuild
from reqconfbot.databases.nethex import NethexJsonDatabase
from reqconfbot.nethexform import ModalFormSetup
from reqconfbot.utils.tools import ErrorsTyper


class NethexCog(Cog):
    COMMANDS_SEPARATOR: ClassVar[str] = ";"
    database: ClassVar[Optional[NethexJsonDatabase]] = None

    def __init__(self, bot: Bot, json_database_folder: Path):
        self.bot = bot
        self.__class__.database = NethexJsonDatabase(json_database_folder)

    @slash_command(name="form_master", description="Отправляет в данный текстовый канал настраиваемое сообщение с кнопок для отправки заявок")
    @has_permissions(administrator=True)
    async def __send_forms_setup_message(self, context: ApplicationContext):
        err = ErrorsTyper("Не удалось отправить мастер-форм, попробуйте сделать следующие шаги:")
        server_data = self.database.get(context.guild_id)

        if server_data.forms_channel_id is None:
            err.add("Задать канал для вывода заявок")

        if server_data.minecraft_commands_channel_id is None:
            err.add("Задать канал для команд")

        if server_data.minecraft_commands_on_player_apply is None:
            err.add("Задать команду при добавлении игрока")

        if err.isFailed():
            await err.respond(context)
            return

        await context.send_modal(ModalFormSetup())

    @slash_command(
        name="commands_player_add",
        description=f"команды при добавлении игрока ({COMMANDS_SEPARATOR} для разделения)"
    )
    @has_permissions(administrator=True)
    async def __set_minecraft_commands_on_player_add(
            self,
            context: ApplicationContext,
            commands: str
    ):
        commands = commands.strip()
        err = ErrorsTyper()

        for placeholder in (NethexGuild.MINECRAFT_PLAYER_NAME_PLACEHOLDER, NethexGuild.DISCORD_USER_ID_PLACEHOLDER):
            if placeholder not in commands:
                err.add(f"Команда должна содержать шаблон для подстановки `{placeholder}`")

        if err.isFailed():
            await err.respond(context)
            return

        self.database.get(context.guild_id).minecraft_commands_on_player_apply = cmds = tuple(filter(bool, commands.split(self.COMMANDS_SEPARATOR)))
        self.database.dump()

        cmd_repr = ''.join(f'* `{c}`\n' for c in cmds)
        await context.respond(f"При одобрении заявки будут выполнены команды:\n{cmd_repr}", ephemeral=True)

    # FIXME Дублирование кода
    @slash_command(name="commands_output")
    @has_permissions(administrator=True)
    async def __set_commands_output(
            self,
            context: ApplicationContext,
            channel: Option(TextChannel, required=True, description="Настроить канал для вывода команд")
    ):
        channel: TextChannel

        self.database.get(context.guild_id).minecraft_commands_channel_id = channel.id
        self.database.dump()

        await context.respond(f"Теперь канал для вывода команд - {channel.jump_url}", ephemeral=True)

    @slash_command(name="forms_output")
    @has_permissions(administrator=True)
    async def __set_forms_send_output(
            self,
            context: ApplicationContext,
            channel: Option(TextChannel, required=True, description="Настроить канал для рассмотрения заявок")
    ):
        channel: TextChannel

        self.database.get(context.guild_id).forms_channel_id = channel.id
        self.database.dump()

        await context.respond(f"Теперь канал для рассмотрения заявок - {channel.jump_url}", ephemeral=True)
