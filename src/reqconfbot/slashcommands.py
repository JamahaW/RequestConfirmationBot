from discord import ApplicationContext
from discord import Option
from discord import TextChannel
from discord.ext.commands import has_permissions

from reqconfbot.core import bot
from reqconfbot.core import logger
from reqconfbot.nethexform import ModalFormSetup
from reqconfbot.tools import StringBuilder


class SlashCommandHandler:

    @staticmethod
    @bot.slash_command(name="setup")
    @has_permissions(administrator=True)
    async def set_forms_send_output(
            context: ApplicationContext,
            channel: Option(TextChannel, required=True, description="Настроить канал для рассмотрения заявок")
    ):
        channel: TextChannel

        sd = bot.servers_data.get(context.guild_id)
        sd.form_channel_id = channel.id
        logger.debug(f"update {sd}")

        bot.servers_data.dump()
        await context.respond(f"Теперь канал для рассмотрения заявок - {channel.jump_url}", ephemeral=True)

    @staticmethod
    @has_permissions(administrator=True)
    @bot.slash_command(name="info")
    async def show_server_data_info(context: ApplicationContext):
        data = bot.servers_data.get(context.guild_id)

        await context.respond(
            (
                StringBuilder("Данные этого сервера")
                .append(f"{data.KEY_SERVER_ID}={data.server_id}")
                .append(f"{data.KEY_FORM_CHANNEL_ID}={data.form_channel_id}")
            ).toString(), ephemeral=True)

    @staticmethod
    @has_permissions(administrator=True)
    @bot.slash_command(name="send", description="Отправляет в данный текстовый канал настраиваемое сообщение с кнопок для отправки заявок")
    async def send_forms_setup_message(context: ApplicationContext):
        await context.send_modal(ModalFormSetup())
