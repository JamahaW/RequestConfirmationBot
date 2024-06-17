from abc import ABC
from logging import DEBUG
from os import getenv

from discord import Bot
from discord import Intents

from reqconfbot.customlogger import CustomFileHandler
from reqconfbot.customlogger import createCustomLogger
from reqconfbot.customlogger import getLogPath
from reqconfbot.tools import envLoad


class CustomDiscordBot(Bot, ABC):
    def __init__(self):
        super().__init__(getenv("DISCORD_BOT_PREFIX"), intents=Intents.default().all())

    def run(self):
        super().run(token=getenv("DISCORD_BOT_TOKEN"))


envLoad((".env", "public.env"))
bot = CustomDiscordBot()
logger = createCustomLogger(__name__, CustomFileHandler(getLogPath(getenv("LOGGING_RELATIVE_FOLDER"))), DEBUG, True)
