from typing import Iterable

from discord.ui import View

from reqconfbot.bots.custombot import CustomBot
from reqconfbot.cogs.nethex import NethexCog
from reqconfbot.cogs.legacy_nethex_form import NethexFormView
from reqconfbot.cogs.legacy_nethex_form import NethexPanelCreatorView
from reqconfbot.utils.tools import Environment


class NethexBot(CustomBot):

    def getPersistentViews(self) -> Iterable[View]:
        return (
            NethexPanelCreatorView(),
            NethexFormView()
        )

    def __init__(self, env: Environment):
        super().__init__(env.prefix)
        self.add_cog(NethexCog(self, env.databases_folder))
