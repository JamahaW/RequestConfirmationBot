from enum import Enum
from enum import auto
from logging import DEBUG
from os import PathLike

from reqconfbot.bots.custombot import CustomBot
from reqconfbot.bots.forbiddenteam import ForbiddenBot
from reqconfbot.bots.nethex import NethexBot
from reqconfbot.utils.customlogger import CustomFileHandler
from reqconfbot.utils.customlogger import createCustomLogger
from reqconfbot.utils.customlogger import createLogFilepath
from reqconfbot.utils.tools import Environment


class BotType(Enum):
    NETHEX = auto()
    FORBIDDEN_TEAM = auto()


def getBot(bot_type: BotType, env: Environment) -> CustomBot:
    match bot_type:
        case BotType.NETHEX:
            return NethexBot(env.prefix, env.database_folder)

        case BotType.FORBIDDEN_TEAM:
            return ForbiddenBot(env)


def launchBot(env_filepath: PathLike | str):
    env = Environment(env_filepath)

    logger = createCustomLogger(__name__, CustomFileHandler(createLogFilepath(env.log_folder)), DEBUG, True)
    logger.info(f"env (public): {env}")

    BOT_TYPE = BotType.FORBIDDEN_TEAM

    bot = getBot(BOT_TYPE, env)
    bot.setLogger(logger)
    bot.run(token=env.token)

    logger.info("quit")
