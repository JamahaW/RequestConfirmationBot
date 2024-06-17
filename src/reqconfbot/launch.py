# USE PYCORD

import os
from logging import DEBUG

import dotenv
from discord import ApplicationContext
from discord import Bot
from discord import Intents
from discord import Member
from discord import Message
from discord import Option

from reqconfbot.customlogger import CustomFileHandler
from reqconfbot.customlogger import createCustomLogger
from reqconfbot.customlogger import getLogPath
from reqconfbot.modals import TestModal
from reqconfbot.views import TestViewButtons2
from reqconfbot.views import TestViewSelectMenu

dotenv.load_dotenv(".env")
__DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

logger = createCustomLogger(__name__, CustomFileHandler(getLogPath("../../logs/")), DEBUG, True)
logger.debug("start!")

bot = Bot("&", intents=(Intents.default().all()))


@bot.event
async def on_ready():
    logger.info(f"{bot.user.name} запустился и готов к работе!")


@bot.event
async def on_message(message: Message):
    if message.author.bot:
        return

    logger.debug(f'Получено сообщение! Сервер: {message.guild} Текст: {message.content}')


@bot.slash_command()
async def button_my_view(ctx):
    await ctx.respond("This is a button!", view=TestViewButtons2())


@bot.slash_command()
async def select_menu_demo(context: ApplicationContext):
    await context.respond("view", view=TestViewSelectMenu())


@bot.slash_command()
async def test_form(context: ApplicationContext):
    await context.send_modal(TestModal(title="Заявка тест"))


@bot.slash_command(name='test_slash_command')
async def __test(
        ctx,
        number: Option(int, description='Число в диапазоне от 1 до 10', required=True, min_value=1, max_value=10),
        member: Option(Member, description='Любой участник сервера', required=True),
        choice: Option(str, description='Выберите пункт из списка', required=True, choices=['Банан', 'Яблоко', 'Апельсин']),
        text: Option(str, description='Текст из нескольких слов', required=False, default=''),
        boolean: Option(bool, description='True или False', required=False, default=False)
):
    await ctx.delete()

    for argument in (number, boolean, member, text, choice):
        logger.debug(f'{argument} ({type(argument).__name__})\n')


if __name__ == '__main__':
    logger.info("Request Confirmation bot")
    bot.run(token=__DISCORD_BOT_TOKEN)
    logger.info("stopped")
