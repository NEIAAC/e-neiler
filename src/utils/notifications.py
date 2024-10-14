from PySide6.QtWidgets import QSystemTrayIcon
from PySide6.QtGui import QIcon, QPixmap

from utils.constants import LOGO_PATH
from utils import path

class Notifications(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        self.setIcon(QIcon(QPixmap(path.fromBase(LOGO_PATH))))

    def send(self, title: str, body: str):
        """Allows sending tray messages with an hidden tray icon."""
        self.setVisible(True)
        self.showMessage(title, body)
        self.setVisible(False)
