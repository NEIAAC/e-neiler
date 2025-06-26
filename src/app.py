from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPixmap

from version import __version__
from utils import file_loader
from utils.logger import logger
from config.metadata import (
    EXECUTABLE_NAME,
    AUTHOR_NAME,
    AUTHOR_DOMAIN,
    LOGO_PATH,
)


class App(QApplication):
    """Base application class."""

    def __init__(self, argv: list[str]):
        super().__init__(argv)

        self.setApplicationName(EXECUTABLE_NAME)
        self.setOrganizationName(AUTHOR_NAME)
        self.setOrganizationDomain(AUTHOR_DOMAIN)
        self.setApplicationVersion(__version__)

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
            logger.info(
                f"|{' ' * padding}{line}{' ' * (length - len(line) + padding)}|"
            )
        logger.info(column)
        logger.info(row)

        self.setWindowIcon(
            QIcon(QPixmap(file_loader.getResourcePath(LOGO_PATH)))
        )
