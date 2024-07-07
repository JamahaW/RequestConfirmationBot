from typing import Iterable

from discord.ui import View

from reqconfbot.bots.custombot import CustomBot
from reqconfbot.cogs.forbiddenteam import ForbiddenCog
from reqconfbot.utils.tools import Environment


class ForbiddenBot(CustomBot):
    def getPersistentViews(self) -> Iterable[View]:
        return tuple[View]()

    def __init__(self, env: Environment) -> None:
        super().__init__(env.prefix)
        self.cog = ForbiddenCog(self, env.databases_folder)
        self.add_cog(self.cog)
        self.db = self.cog.database
