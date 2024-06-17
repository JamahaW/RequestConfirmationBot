from __future__ import annotations

import sys
from datetime import datetime
from logging import DEBUG
from logging import FileHandler
from logging import Formatter
from logging import Logger
from logging import StreamHandler
from logging import getLogger
from typing import Final

from reqconfbot.datetimehelper import TIME_FORMAT
from reqconfbot.datetimehelper import datetimeString


class CustomFileHandler(FileHandler):
    MESSAGE_FORMAT: Final[str] = "%(asctime)s:[%(levelname)s]:%(funcName)s:%(lineno)d: %(message)s"

    def __init__(self, logfile: str) -> None:
        super().__init__(logfile, mode="w")
        self.setFormatter(Formatter(self.MESSAGE_FORMAT, datefmt=TIME_FORMAT))


def createCustomLogger(name: str, filehandler: FileHandler, level: int = DEBUG, send_stdout: bool = False) -> Logger:
    logger = getLogger(name)
    logger.setLevel(level)
    logger.addHandler(filehandler)

    if send_stdout:
        logger.addHandler(StreamHandler(sys.stdout))

    return logger


def getLogPath(path: str) -> str:
    return f"{path}{datetimeString(datetime.now())}.log"
