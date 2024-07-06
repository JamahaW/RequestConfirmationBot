from abc import ABC
from logging import DEBUG
from os import getenv

from discord import Bot
from discord import Intents
from discord import Message
from dotenv import load_dotenv

from reqconfbot.cogs.example import Example
from reqconfbot.customlogger import CustomFileHandler
from reqconfbot.customlogger import createCustomLogger
from reqconfbot.customlogger import getLogPath
from reqconfbot.jsondatabase import ServerJSONDatabase
from reqconfbot.nethexform import ViewSendModalRequest
from reqconfbot.nethexform import ViewUserForm


class CustomDiscordBot(Bot, ABC):
    def __init__(self):
        super().__init__(getenv("DISCORD_BOT_PREFIX"), intents=Intents.default().all())
        self.__persistent_views_added = False

        db = ServerJSONDatabase(getenv("JSON_DATABASE_PATH"))
        self.servers_data = db
        ViewSendModalRequest.server_database = db
        ViewUserForm.server_database = db

    def run(self):
        super().run(token=getenv("DISCORD_BOT_TOKEN"))

    async def on_ready(self):
        logger.info(f"{bot.user.name} запустился и готов к работе!")

        if not self.__persistent_views_added:
            self.__persistent_views_added = True
            self.addPersistentViews()
            logger.info("persistent_views_added")

    def addPersistentViews(self):
        self.add_view(ViewSendModalRequest())
        self.add_view(ViewUserForm())

    @staticmethod
    async def on_message(message: Message):
        if message.author.bot:
            return


load_dotenv("./reqconfbot/.env")

bot = CustomDiscordBot()
bot.add_cog(Example(bot))

logger = createCustomLogger(__name__, CustomFileHandler(getLogPath(getenv("LOG_FOLDER"))), DEBUG, True)
