from dataclasses import dataclass
from dataclasses import field
from logging import DEBUG
from os import PathLike
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from reqconfbot.bots.nethex import NethexBot
from reqconfbot.customlogger import CustomFileHandler
from reqconfbot.customlogger import createCustomLogger
from reqconfbot.customlogger import createLogFilepath


@dataclass()
class EnvironmentData:
    log_folder: Path
    database_folder: Path
    prefix: str
    token: str = field(repr=False)

    def __init__(self, env_filepath: PathLike | str) -> None:
        load_dotenv(env_filepath)
        self.log_folder = Path(getenv("LOG_FOLDER"))
        self.database_folder = Path(getenv("JSON_DATABASE_PATH"))
        self.prefix = getenv("DISCORD_BOT_PREFIX")
        self.token = getenv("DISCORD_BOT_TOKEN")


def launchBot(env_filepath: PathLike | str):
    env = EnvironmentData(env_filepath)

    logger = createCustomLogger(__name__, CustomFileHandler(createLogFilepath(env.log_folder)), DEBUG, True)

    logger.info(f"env (public): {env}")

    bot = NethexBot(logger, env.prefix, env.database_folder)
    bot.run(token=env.token)

    logger.info("quit")
