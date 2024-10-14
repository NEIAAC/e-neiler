import os
import sys

from loguru import logger

from utils.constants import DATA_PATH

LOGS_PATH = os.path.join(DATA_PATH, "logs")

formatter = "[{time:YYYY-MM-DDTHH:mm:ss.SSS[Z]!UTC}] [<level>{level}</level>] {message}"

dev = "__compiled__" not in globals()

logger.remove()
logger.level("INFO", color="<green>")

if dev:
    logger.add(sys.stdout, colorize=True, format=formatter, level="DEBUG")

logger.add(os.path.join(LOGS_PATH, "{time:YYYY-MM-DD!UTC}.log".replace("\\", "/")),
           format=formatter,
           rotation="00:00",
           retention="30 days",
           level="DEBUG" if dev else "INFO")
