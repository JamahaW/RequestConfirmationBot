import os
from abc import ABC
from logging import DEBUG

from discord import Bot
from discord import Intents
from dotenv import load_dotenv

from reqconfbot.customlogger import CustomFileHandler
from reqconfbot.customlogger import createCustomLogger
from reqconfbot.customlogger import getLogPath


class CustomDiscordBot(Bot, ABC):
    def __init__(self, prefix: str):
        super().__init__(prefix, intents=Intents.default().all())
        load_dotenv(".env")

    def run(self):
        super().run(token=os.getenv("DISCORD_BOT_TOKEN"))


logger = createCustomLogger(__name__, CustomFileHandler(getLogPath("../../logs/")), DEBUG, True)

bot = CustomDiscordBot("&")

logger.debug("start!")
