import datetime
import os
import sys

from loguru import logger
from PySide6 import QtCore

from config.metadata import DATA_PATH

LOGS_PATH = os.path.join(DATA_PATH, "logs")

formatter = (
    "[{time:YYYY-MM-DDTHH:mm:ss.SSS[Z]!UTC}] [<level>{level}</level>] {message}"
)

dev = "__compiled__" not in globals()

logger.remove()
logger.level("INFO", color="<green>")

if dev:
    logger.add(
        sys.stdout, colorize=True, format=formatter, level="DEBUG", enqueue=True
    )

logger.add(
    os.path.join(LOGS_PATH, "{time:YYYY-MM-DD!UTC}.log".replace("\\", "/")),
    format=formatter,
    rotation=datetime.time(0, 0, 0, tzinfo=datetime.timezone.utc),
    retention="30 days",
    enqueue=True,
    level="DEBUG" if dev else "INFO",
)


def qMessageHandler(
    mode: QtCore.QtMsgType, _: QtCore.QMessageLogContext, message: str
):
    match mode:
        case QtCore.QtMsgType.QtInfoMsg:
            logger.info(message)
        case QtCore.QtMsgType.QtWarningMsg:
            logger.warning(message)
        case QtCore.QtMsgType.QtCriticalMsg:
            logger.error(message)
        case QtCore.QtMsgType.QtFatalMsg:
            logger.critical(message)
        case _:
            logger.debug(message)
