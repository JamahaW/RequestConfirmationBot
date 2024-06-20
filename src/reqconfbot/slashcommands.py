from discord import ApplicationContext
from discord import Member
from discord import Option
from discord import TextChannel
from discord.ext.commands import has_permissions
from discord.ui import View

from reqconfbot.buttons import CounterButton
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
    @bot.slash_command()
    async def send_forms_setup_message(context: ApplicationContext):
        await context.send_modal(ModalFormSetup())

    @staticmethod
    @bot.slash_command()
    async def test_slash_command_args(
            context: ApplicationContext,
            number: Option(int, description='Число в диапазоне от 1 до 10', required=True, min_value=1, max_value=10),
            member: Option(Member, description='Любой участник сервера', required=True),
            choice: Option(str, description='Выберите пункт из списка', required=True, choices=['Банан', 'Яблоко', 'Апельсин']),
            text: Option(str, description='Текст из нескольких слов', required=False, default=''),
            boolean: Option(bool, description='True или False', required=False, default=False)
    ):
        await context.delete()

        for argument in (number, boolean, member, text, choice):
            logger.debug(f'{argument} ({type(argument).__name__})\n')

    @staticmethod
    @bot.slash_command()
    async def test_button_counter(
            context: ApplicationContext,
            counter_text: Option(str, description="Текст счётчика", default=None)
    ):
        await context.respond(view=View(
            CounterButton(counter_text),
            timeout=None
        ))
