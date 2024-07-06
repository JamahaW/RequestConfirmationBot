from pathlib import Path
from typing import Iterable

from discord.ui import View

from reqconfbot.bots.custombot import CustomBot
from reqconfbot.cogs.nethex import NethexCog
from reqconfbot.legacy_nethex_form import NethexFormView
from reqconfbot.legacy_nethex_form import NethexPanelCreatorView


class NethexBot(CustomBot):

    def getPersistentViews(self) -> Iterable[View]:
        return (
            NethexPanelCreatorView(),
            NethexFormView()
        )

    def __init__(self, prefix: str, json_database_folder: Path):
        super().__init__(prefix)
        self.add_cog(NethexCog(self, json_database_folder))
