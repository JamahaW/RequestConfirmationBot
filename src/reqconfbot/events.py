from discord import Message

from reqconfbot.core import bot
from reqconfbot.core import logger


class DiscordBotEventHandler:

    @staticmethod
    @bot.event
    async def on_ready():
        logger.info(f"{bot.user.name} запустился и готов к работе!")

    @staticmethod
    @bot.event
    async def on_message(message: Message):
        if message.author.bot:
            return

        logger.debug(f'Получено сообщение! Сервер: {message.guild} Текст: {message.content}')
