from abc import ABC
from logging import DEBUG
from os import getenv

from discord import Bot
from discord import Intents
from discord import Message

from reqconfbot.customlogger import CustomFileHandler
from reqconfbot.customlogger import createCustomLogger
from reqconfbot.customlogger import getLogPath
from reqconfbot.jsondatabase import ServerJSONDatabase
from reqconfbot.nethexform import ViewSendModalRequest
from reqconfbot.tools import envLoad


class CustomDiscordBot(Bot, ABC):
    def __init__(self):
        super().__init__(getenv("DISCORD_BOT_PREFIX"), intents=Intents.default().all())
        self.persistent_views_added = False

        self.servers_data = ServerJSONDatabase(getenv("SERVERS_JSON_DATABASE_PATH"))

    def run(self):
        super().run(token=getenv("DISCORD_BOT_TOKEN"))

    async def on_ready(self):
        logger.info(f"{bot.user.name} запустился и готов к работе!")

        if not self.persistent_views_added:
            self.persistent_views_added = True
            self.add_view(ViewSendModalRequest())

    async def on_message(self, message: Message):
        if message.author.bot:
            return

        logger.debug(f'Получено сообщение! Сервер: {message.guild} Текст: {message.content}')


envLoad((".env", "public.env"))
bot = CustomDiscordBot()
logger = createCustomLogger(__name__, CustomFileHandler(getLogPath(getenv("LOGGING_RELATIVE_FOLDER"))), DEBUG, True)
