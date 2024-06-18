from abc import ABC
from logging import DEBUG
from os import getenv

from discord import Bot
from discord import Intents
from discord import Message

from reqconfbot.customlogger import CustomFileHandler
from reqconfbot.customlogger import createCustomLogger
from reqconfbot.customlogger import getLogPath
from reqconfbot.tools import envLoad
from reqconfbot.views import PersistentView


class CustomDiscordBot(Bot, ABC):
    def __init__(self):
        super().__init__(getenv("DISCORD_BOT_PREFIX"), intents=Intents.default().all())
        self.persistent_views_added = False

    def run(self):
        super().run(token=getenv("DISCORD_BOT_TOKEN"))

    async def on_ready(self):
        logger.info(f"{bot.user.name} запустился и готов к работе!")

        if not self.persistent_views_added:
            # Register the persistent view for listening here.
            # Note that this does not send the view to any message.
            # In order to do this you need to first send a message with the View, which is shown below.
            # If you have the message_id you can also pass it as a keyword argument,
            # but for this example we don't have one.
            self.add_view(PersistentView())
            self.persistent_views_added = True

    async def on_message(self, message: Message):
        if message.author.bot:
            return

        logger.debug(f'Получено сообщение! Сервер: {message.guild} Текст: {message.content}')


envLoad((".env", "public.env"))
bot = CustomDiscordBot()
logger = createCustomLogger(__name__, CustomFileHandler(getLogPath(getenv("LOGGING_RELATIVE_FOLDER"))), DEBUG, True)
