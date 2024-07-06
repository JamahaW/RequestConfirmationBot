from logging import DEBUG
from os import PathLike

from reqconfbot.bots.nethex import NethexBot
from reqconfbot.customlogger import CustomFileHandler
from reqconfbot.customlogger import createCustomLogger
from reqconfbot.customlogger import createLogFilepath
from reqconfbot.tools import EnvironmentData


def launchBot(env_filepath: PathLike | str):
    env = EnvironmentData(env_filepath)

    logger = createCustomLogger(__name__, CustomFileHandler(createLogFilepath(env.log_folder)), DEBUG, True)

    logger.info(f"env (public): {env}")

    bot = NethexBot(logger, env.prefix, env.database_folder)
    bot.run(token=env.token)

    logger.info("quit")
