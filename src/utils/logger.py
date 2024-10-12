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

    def namer(name: str):
        dir, file = os.path.split(name)
        _, timestamp = file.rsplit(".", 1)
        return os.path.join(dir, f"{timestamp}.log")

    file = logging.handlers.TimedRotatingFileHandler(
        os.path.join(path, "{:%Y-%m-%d}.log".format(datetime.datetime.now(tz=datetime.timezone.utc).date())),
        backupCount=30,
        when="midnight",
        delay=True,
        utc=True)
    file.setFormatter(formatter)
    file.namer = namer

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    dev = "__compiled__" not in globals()

    logging.basicConfig(
        level=logging.DEBUG if dev else logging.INFO,
        handlers=[console, file] if dev else [file],
        format=syntax)

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
