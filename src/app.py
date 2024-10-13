import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QStandardPaths
from PySide6.QtGui import QIcon, QPixmap

APP_NAME = "E-neiler"
AUTHOR_NAME = "NEIAAC"
AUTHOR_DOMAIN = "neiaac.com"
LOGO_PATH = "resources/icons/logo.png"
DATA_PATH = os.path.join(os.path.join((QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)),
    AUTHOR_NAME, APP_NAME))

from version import __version__
from utils import path
from utils.logger import logger

class App(QApplication):
    def __init__(self, argv: list[str]):
        super().__init__(argv)

        self.setApplicationName(APP_NAME)
        self.setOrganizationName(AUTHOR_NAME)
        self.setOrganizationDomain(AUTHOR_DOMAIN)
        self.setApplicationVersion(__version__)
        self.setWindowIcon(QIcon(QPixmap(path.fromBase(LOGO_PATH))))
        self.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

        data = [
            self.applicationName(),
            "",
            self.applicationVersion(),
        ]

        length = max(len(value) for value in data)
        padding = 2
        row = f"+{'-' * (length + padding * 2)}+"
        column = f"|{' ' * (length + padding * 2)}|"

        logger.info(row)
        logger.info(column)
        for line in data:
            logger.info(f"|{' ' * padding}{line}{' ' * (length - len(line) + padding)}|")
        logger.info(column)
        logger.info(row)
