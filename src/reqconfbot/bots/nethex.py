from logging import Logger
from os import PathLike
from typing import Iterable

from discord.ui import View

from reqconfbot.bots.base import CustomBot
from reqconfbot.cogs.nethex import NethexCog
from reqconfbot.nethexform import ViewSendModalRequest
from reqconfbot.nethexform import ViewUserForm


class NethexBot(CustomBot):

    def getPersistentViews(self) -> Iterable[View]:
        return (
            ViewSendModalRequest(),
            ViewUserForm()
        )

    def __init__(self, logger: Logger, prefix: str, json_database_path: PathLike | str):
        super().__init__(logger, prefix)
        self.add_cog(NethexCog(self, json_database_path))
