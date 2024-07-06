from os import PathLike
from typing import Final

from discord import ApplicationContext
from discord import Bot
from discord import Option
from discord import TextChannel
from discord.ext.commands import Cog
from discord.ext.commands import has_permissions
from discord.ext.commands import slash_command

from reqconfbot.jsondatabase import ServerData
from reqconfbot.jsondatabase import ServerJSONDatabase
from reqconfbot.nethexform import ModalFormSetup
from reqconfbot.nethexform import ViewSendModalRequest
from reqconfbot.nethexform import ViewUserForm
from reqconfbot.tools import ErrorsTyper


class NethexCog(Cog):
    COMMANDS_SEPARATOR: Final[str] = ";"

    def __init__(self, bot: Bot, json_database_path: PathLike | str):
        self.bot = bot
        db = ServerJSONDatabase(json_database_path)
        self.servers_data = db
        ViewSendModalRequest.server_database = db
        ViewUserForm.server_database = db

    @slash_command()
    async def nethex_cog_test(self, context: ApplicationContext):
        await context.respond("nethex_cog_test")

    @slash_command(name="form_master", description="Отправляет в данный текстовый канал настраиваемое сообщение с кнопок для отправки заявок")
    @has_permissions(administrator=True)
    async def __send_forms_setup_message(self, context: ApplicationContext):
        err = ErrorsTyper("Не удалось отправить мастер-форм, попробуйте сделать следующие шаги:")
        server_data = self.servers_data.get(context.guild_id)

        if server_data.form_channel_id is None:
            err.add("Задать канал для вывода заявок")

        if server_data.commands_send_channel_id is None:
            err.add("Задать канал для команд")

        if server_data.commands_on_player_add is None:
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

        for placeholder in ServerData.MINECRAFT_COMMAND_PLACEHOLDERS:
            if placeholder not in commands:
                err.add(f"Команда должна содержать шаблон для подстановки (значение после =) {placeholder}")

        if err.isFailed():
            await err.respond(context)
            return

        self.servers_data.get(context.guild_id).commands_on_player_add = cmds = tuple(filter(bool, commands.split(self.COMMANDS_SEPARATOR)))
        self.servers_data.dump()

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

        self.servers_data.get(context.guild_id).commands_send_channel_id = channel.id
        self.servers_data.dump()

        await context.respond(f"Теперь канал для вывода команд - {channel.jump_url}", ephemeral=True)

    @slash_command(name="forms_output")
    @has_permissions(administrator=True)
    async def __set_forms_send_output(
            self,
            context: ApplicationContext,
            channel: Option(TextChannel, required=True, description="Настроить канал для рассмотрения заявок")
    ):
        channel: TextChannel

        self.servers_data.get(context.guild_id).form_channel_id = channel.id
        self.servers_data.dump()

        await context.respond(f"Теперь канал для рассмотрения заявок - {channel.jump_url}", ephemeral=True)
