from logging import Logger
from pathlib import Path
from typing import Iterable

from discord.ui import View

from reqconfbot.bots import CustomBot
from reqconfbot.cogs.nethex import NethexCog
from reqconfbot.forms.nethex import CreatePanelView
from reqconfbot.forms.nethex import NethexFormView


class NethexBot(CustomBot):

    def getPersistentViews(self) -> Iterable[View]:
        return (
            CreatePanelView(),
            NethexFormView()
        )

    def __init__(self, logger: Logger, prefix: str, json_database_folder: Path):
        super().__init__(logger, prefix)
        self.add_cog(NethexCog(self, json_database_folder))
