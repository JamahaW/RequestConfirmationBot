from __future__ import annotations

from enum import Enum
from enum import auto
from logging import Logger

from reqconfbot.bots.basicbot import CustomBot
from reqconfbot.bots.nethex import NethexBot
from reqconfbot.tools import Environment


class BotType(Enum):
    NETHEX = auto()

    @classmethod
    def make(cls, bot_type: BotType, logger: Logger, env: Environment) -> CustomBot:
        match bot_type:
            case cls.NETHEX:
                return NethexBot(logger, env.prefix, env.database_folder)

            case _:
                raise ValueError()
