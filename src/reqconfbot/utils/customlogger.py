from __future__ import annotations

import sys
from datetime import datetime
from logging import DEBUG
from logging import FileHandler
from logging import Formatter
from logging import Logger
from logging import StreamHandler
from logging import getLogger
from os import PathLike
from pathlib import Path
from typing import Final

from reqconfbot.utils.tools import TIME_FORMAT
from reqconfbot.utils.tools import datetimeString


class CustomFileHandler(FileHandler):
    MESSAGE_FORMAT: Final[str] = "%(asctime)s:[%(levelname)s]:%(funcName)s:%(lineno)d: %(message)s"

    def __init__(self, logfile: PathLike | str) -> None:
        super().__init__(logfile, mode="w")
        self.setFormatter(Formatter(self.MESSAGE_FORMAT, datefmt=TIME_FORMAT))


def createCustomLogger(name: str, filehandler: FileHandler, level: int = DEBUG, send_stdout: bool = False) -> Logger:
    __logger = getLogger(name)
    __logger.setLevel(level)
    __logger.addHandler(filehandler)

    if send_stdout:
        __logger.addHandler(StreamHandler(sys.stdout))

    return __logger


def createLogFilepath(path: Path) -> Path:
    return path / f"{datetimeString(datetime.now())}.log"
