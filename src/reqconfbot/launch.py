from logging import DEBUG
from os import PathLike

from reqconfbot.bots.nethex import NethexBot
from reqconfbot.utils.customlogger import CustomFileHandler
from reqconfbot.utils.customlogger import createCustomLogger
from reqconfbot.utils.customlogger import createLogFilepath
from reqconfbot.utils.tools import Environment


def launchBot(env_filepath: PathLike | str):
    env = Environment(env_filepath)

    logger = createCustomLogger(__name__, CustomFileHandler(createLogFilepath(env.log_folder)), DEBUG, True)
    logger.info(f"env (public): {env}")

    bot = NethexBot(env.prefix, env.database_folder)
    bot.setLogger(logger)
    bot.run(token=env.token)

    logger.info("quit")
