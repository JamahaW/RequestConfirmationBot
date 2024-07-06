from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from logging import Logger
from typing import Iterable
from typing import Optional

from discord import Bot
from discord import Intents
from discord import Message
from discord.ui import View


class CustomBot(Bot, ABC):
    def __init__(self, prefix: str):
        super().__init__(prefix, intents=Intents.default().all())
        self.__persistent_views_added = False
        self.logger: Optional[Logger] = None

    def setLogger(self, logger: Logger) -> None:
        self.logger = logger

    async def on_ready(self):
        self.logger.info(f"{self.user.name} запустился и готов к работе!")

        if not self.__persistent_views_added:
            for v in self.getPersistentViews():
                self.add_view(v)

            self.__persistent_views_added = True
            self.logger.info("persistent_views_added")

    @staticmethod
    async def on_message(message: Message):
        if message.author.bot:
            return

    @abstractmethod
    def getPersistentViews(self) -> Iterable[View]:
        pass
