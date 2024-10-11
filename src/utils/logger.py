import datetime
import sys, os, logging, logging.handlers
import traceback
from contextlib import contextmanager

from PySide6.QtCore import QStandardPaths

class Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        timestamp = datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc)
        return timestamp.strftime(datefmt) if datefmt else timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def setup():
    """
    Sets up the root logger to the respective QT platform-specific folder, based on the organization and app name.\n
    Development: logs to stdout and file.\n
    Compiled: logs only to file.\n
    """

    path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation), "logs")

    if not os.path.exists(path):
        os.makedirs(path)

    syntax = "[%(asctime)s] [%(levelname)s] %(message)s"

    formatter = Formatter(syntax)

    def filename(): return "{:%Y-%m-%d}.log".format(datetime.datetime.now(tz=datetime.timezone.utc).date())
    file = logging.handlers.TimedRotatingFileHandler(os.path.join(path, filename()), backupCount=30, when="midnight", utc=True)
    file.namer = lambda _: filename()
    file.setFormatter(formatter)

    dev = "__compiled__" not in globals()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if dev else logging.INFO)
    logger.addHandler(file)

    if dev:
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    sys.excepthook = lambda exctype, value, tb: logging.error("".join(traceback.format_exception(exctype, value, tb)))

@contextmanager
def suppressor():
    """
    Suppresses stdout output when used as a context manager.
    """
    with open(os.devnull, "w") as devnull:
        old = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old
