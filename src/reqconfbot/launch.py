from typing import Final

from discord import ApplicationContext
from discord import Option
from discord import TextChannel
from discord.ext.commands import has_permissions

from reqconfbot.core import bot
from reqconfbot.core import logger
from reqconfbot.jsondatabase import ServerData
from reqconfbot.nethexform import ModalFormSetup
from reqconfbot.tools import ErrorsTyper


def launchBot():
    bot.run()
    logger.info("stopped")


@bot.slash_command(name="form_master", description="Отправляет в данный текстовый канал настраиваемое сообщение с кнопок для отправки заявок")
@has_permissions(administrator=True)
async def __send_forms_setup_message(context: ApplicationContext):
    err = ErrorsTyper("Не удалось отправить мастер-форм, попробуйте сделать следующие шаги:")
    server_data = bot.servers_data.get(context.guild_id)

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


COMMANDS_SEPARATOR: Final[str] = ";"


@bot.slash_command(
    name="commands_player_add",
    description=f"команды при добавлении игрока ({COMMANDS_SEPARATOR} для разделения)"
)
@has_permissions(administrator=True)
async def __set_minecraft_commands_on_player_add(
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

    bot.servers_data.get(context.guild_id).commands_on_player_add = cmds = tuple(filter(bool, commands.split(COMMANDS_SEPARATOR)))
    bot.servers_data.dump()

    cmd_repr = ''.join(f'* `{c}`\n' for c in cmds)
    await context.respond(f"При одобрении заявки будут выполнены команды:\n{cmd_repr}", ephemeral=True)


# FIXME Дублирование кода
@bot.slash_command(name="commands_output")
@has_permissions(administrator=True)
async def __set_commands_output(
        context: ApplicationContext,
        channel: Option(TextChannel, required=True, description="Настроить канал для вывода команд")
):
    channel: TextChannel

    bot.servers_data.get(context.guild_id).commands_send_channel_id = channel.id
    bot.servers_data.dump()

    await context.respond(f"Теперь канал для вывода команд - {channel.jump_url}", ephemeral=True)


@bot.slash_command(name="forms_output")
@has_permissions(administrator=True)
async def __set_forms_send_output(
        context: ApplicationContext,
        channel: Option(TextChannel, required=True, description="Настроить канал для рассмотрения заявок")
):
    channel: TextChannel

    bot.servers_data.get(context.guild_id).form_channel_id = channel.id
    bot.servers_data.dump()

    await context.respond(f"Теперь канал для рассмотрения заявок - {channel.jump_url}", ephemeral=True)
