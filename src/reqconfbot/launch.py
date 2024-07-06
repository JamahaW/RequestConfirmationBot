from logging import DEBUG
from os import PathLike
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from reqconfbot.bots.nethex import NethexBot
from reqconfbot.customlogger import CustomFileHandler
from reqconfbot.customlogger import createCustomLogger
from reqconfbot.customlogger import createLogFilepath


def launchBot(env_filepath: PathLike | str):
    load_dotenv(env_filepath)
    log_folder = Path(getenv("LOG_FOLDER"))
    prefix = getenv("DISCORD_BOT_PREFIX")
    json_database_path = Path(getenv("JSON_DATABASE_PATH"))

    logger = createCustomLogger(__name__, CustomFileHandler(createLogFilepath(log_folder)), DEBUG, True)

    bot = NethexBot(logger, prefix, json_database_path)
    bot.run(token=getenv("DISCORD_BOT_TOKEN"))

    logger.info("quit")
