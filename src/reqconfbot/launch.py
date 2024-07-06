from discord import ApplicationContext
from discord import Option
from discord import TextChannel
from discord.ext.commands import has_permissions

from reqconfbot.core import bot
from reqconfbot.core import logger
from reqconfbot.jsondatabase import ServerData
from reqconfbot.nethexform import ModalFormSetup
from reqconfbot.tools import ErrorsTyper
from reqconfbot.tools import StringBuilder


def launchBot():
    logger.info("Request Confirmation bot")
    bot.run()
    logger.info("stopped")


@bot.slash_command(name="form_master", description="Отправляет в данный текстовый канал настраиваемое сообщение с кнопок для отправки заявок")
@has_permissions(administrator=True)
async def __send_forms_setup_message(context: ApplicationContext):
    err = ErrorsTyper("Не удалось отправить мастер-форм, попробуйте сделать следующие шаги:")
    server_data = bot.servers_data.get(context.guild_id)

    if server_data.form_channel_id is None:
        err.add("Задать канал для вывода заявок")

    if server_data.command_send_channel_id is None:
        err.add("Задать канал для команд")

    if server_data.command_on_player_add is None:
        err.add("Задать команду при добавлении игрока")

    if err.isFailed():
        await context.respond(str(err), ephemeral=True)
        return

    await context.send_modal(ModalFormSetup())


@bot.slash_command(name="info")
@has_permissions(administrator=True)
async def __show_server_data_info(context: ApplicationContext):
    data = bot.servers_data.get(context.guild_id)

    await context.respond(
        (
            StringBuilder("Данные этого сервера")
            .append(f"{data.SERVER_ID}=`{data.server_id}`")
            .append(f"{data.FORM_CHANNEL_ID}=`{data.form_channel_id}`")
            .append(f"{data.MINECRAFT_COMMAND_ON_PLAYER_ADD}=`{data.command_on_player_add}`")
            .append(f"{data.COMMAND_SEND_CHANNEL_ID}=`{data.command_send_channel_id}`")
        ).toString(), ephemeral=True)


@bot.slash_command(name="command_player_add", description="Укажите, какая команда будет отправляться на сервер Майнкрафт для добавления игрока")
@has_permissions(administrator=True)
async def __set_minecraft_command_on_player_add(
        context: ApplicationContext,
        command_value: str
):
    command_value = command_value.strip()
    err = ErrorsTyper()

    if (p := ServerData.MINECRAFT_COMMAND_PLAYER_PLACEHOLDER) not in command_value:
        err.add(f"Команда должна содержать не менее одного {p} для замены на ник игрока")

    if err.isFailed():
        await context.respond(str(err), ephemeral=True)
        return

    bot.servers_data.get(context.guild_id).command_on_player_add = command_value
    bot.servers_data.dump()

    await context.respond(f"Теперь добавления игроков используется команда вида\n```{command_value}```", ephemeral=True)


# FIXME Дублирование кода
@bot.slash_command(name="commands_output")
@has_permissions(administrator=True)
async def __set_commands_output(
        context: ApplicationContext,
        channel: Option(TextChannel, required=True, description="Настроить канал для вывода команд")
):
    channel: TextChannel

    bot.servers_data.get(context.guild_id).command_send_channel_id = channel.id
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
