from PySide6.QtWidgets import QSystemTrayIcon
from PySide6.QtGui import QIcon, QPixmap

from config.metadata import LOGO_PATH
from utils import file_loader


class SystemTray(QSystemTrayIcon):
    """Class to access system tray/notification functionality."""

    def __init__(self, visible: bool = False):
        super().__init__()

        self.setIcon(QIcon(QPixmap(file_loader.loadResource(LOGO_PATH))))
        self.setVisible(visible)
