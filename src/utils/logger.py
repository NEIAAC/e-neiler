import os
import sys

from loguru import logger

from app import DATA_PATH

path = os.path.join(DATA_PATH, "logs")

formatter = "[{time:YYYY-MM-DDTHH:mm:ss.SSS[Z]}] [<level>{level}</level>] {message}"

dev = "__compiled__" not in globals()

logger.remove()
logger.level("INFO", color="<green>")

if dev:
    logger.add(sys.stdout, colorize=True, format=formatter, level="DEBUG")

logger.add(os.path.join(path, "{time:YYYY-MM-DD!UTC}.log".replace("\\", "/")),
           format=formatter,
           rotation="1 day",
           retention="30 days",
           compression="zip",
           level="DEBUG" if dev else "INFO")
