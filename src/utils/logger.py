import datetime
from enum import Enum
import os
import sys

from loguru import logger
from PySide6 import QtCore

from config.metadata import DATA_PATH

LOGS_PATH = os.path.join(DATA_PATH, "logs")


class LogLevel(Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


formatter = (
    "[{time:YYYY-MM-DDTHH:mm:ss.SSS[Z]!UTC}] [<level>{level}</level>] {message}"
)

trace = "__compiled__" not in globals() or "--debug" in sys.argv[1:]

logger.remove()
logger.level(LogLevel.INFO.value, color="<green>")

if trace:
    logger.add(
        sys.stdout,
        colorize=True,
        format=formatter,
        level=LogLevel.TRACE.value,
        enqueue=True,
    )

logger.add(
    os.path.join(LOGS_PATH, "{time:YYYY-MM-DD!UTC}.log".replace("\\", "/")),
    format=formatter,
    rotation=datetime.time(0, 0, 0, tzinfo=datetime.timezone.utc),
    retention="30 days",
    enqueue=True,
    level=LogLevel.TRACE.value if trace else LogLevel.INFO.value,
)


def qMessageHandler(
    mode: QtCore.QtMsgType, _: QtCore.QMessageLogContext, message: str
):
    match mode:
        case QtCore.QtMsgType.QtDebugMsg:
            logger.debug(message)
        case QtCore.QtMsgType.QtInfoMsg:
            logger.debug(message)
        case QtCore.QtMsgType.QtWarningMsg:
            logger.warning(message)
        case QtCore.QtMsgType.QtCriticalMsg:
            logger.error(message)
        case QtCore.QtMsgType.QtFatalMsg:
            logger.critical(message)
        case _:
            logger.trace(message)
