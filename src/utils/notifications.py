from PySide6.QtWidgets import QSystemTrayIcon
from PySide6.QtGui import QIcon, QPixmap

from app import LOGO_PATH

class Notifications(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        self.setIcon(QIcon(QPixmap(LOGO_PATH)))

    def send(self, title, body):
        """Allows sending tray messages with an hidden tray icon."""
        self.setVisible(True)
        self.showMessage(title, body)
        self.setVisible(False)
