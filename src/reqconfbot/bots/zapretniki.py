from typing import Iterable

from discord.ui import View

from reqconfbot.bots.custombot import CustomBot
from reqconfbot.cogs.zapretniki import ZapretnikiCog
from reqconfbot.special.zapretniki import TaskView
from reqconfbot.utils.tools import Environment


class ZapretnikiBot(CustomBot):
    def getPersistentViews(self) -> Iterable[View]:
        return (
            TaskView(),
        )

    def __init__(self, env: Environment) -> None:
        super().__init__(env.prefix)
        self.add_cog(ZapretnikiCog(self, env.databases_folder))
