import logging
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QStandardPaths
from PySide6.QtGui import QIcon, QPixmap

from utils.logger import suppressor
with suppressor():
    from qfluentwidgets import QConfig, qconfig

from version import __version__
from utils import path, logger, config

LOGO_PATH = "resources/icons/logo.png"

class App(QApplication):
    def __init__(self, argv: list[str]):
        super().__init__(argv)

        self.setApplicationName("E-neiler")
        self.setOrganizationName("NEIAAC")
        self.setOrganizationDomain("neiaac.com")
        self.setApplicationVersion(__version__)
        self.setLogger(logger.setup)
        self.setConfig(config.customizable)
        self.setWindowIcon(QIcon(QPixmap(path.fromBase(LOGO_PATH))))
        self.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    def setLogger(self, setup: callable):
        """
        Calls a setup function that is expected to configure the root logger.
        The root logger is then used to log information about the application at startup.
        """
        setup()

        data = [
            self.applicationName(),
            "",
            self.applicationVersion(),
        ]

        length = max(len(value) for value in data)
        padding = 2
        row = f"+{'-' * (length + padding * 2)}+"
        column = f"|{' ' * (length + padding * 2)}|"

        logging.info(row)
        logging.info(column)
        for line in data:
            logging.info(f"|{' ' * padding}{line}{' ' * (length - len(line) + padding)}|")
        logging.info(column)
        logging.info(row)

    def setConfig(self, config: QConfig):
        file = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation), "config.json")
        if os.path.exists(file):
            logging.info(f"Config file found")
        else:
            logging.info(f"Config file not found, using defaults")
        qconfig.load(file, config)
        logging.info(f"Config initialized")
