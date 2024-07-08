from logging import DEBUG

from reqconfbot.bots.custombot import CustomBot
from reqconfbot.utils.customlogger import CustomFileHandler
from reqconfbot.utils.customlogger import createCustomLogger
from reqconfbot.utils.customlogger import createLogFilepath
from reqconfbot.utils.tools import Environment


def launchBot(bot: CustomBot, env: Environment):
    logger = createCustomLogger(__name__, CustomFileHandler(createLogFilepath(env.log_folder)), DEBUG, True)
    logger.info(f"env (public): {env}")

    bot.setLogger(logger)
    bot.run(token=env.token)

    logger.info("quit")
