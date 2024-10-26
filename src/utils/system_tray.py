from PySide6.QtWidgets import QSystemTrayIcon
from PySide6.QtGui import QIcon, QPixmap

from utils.constants import LOGO_PATH
from utils import loader


class SystemTray(QSystemTrayIcon):
    """Class to access system tray/notification functionality."""

    def __init__(self, visible: bool = False):
        super().__init__()

        self.setIcon(QIcon(QPixmap(loader.resources(LOGO_PATH))))
        self.setVisible(visible)

    def send(self, title: str, body: str, messageClicked: callable = None):
        """Allows sending tray messages without showing an icon in the system tray."""
        self.messageClicked.connect(messageClicked)
        visible = self.isVisible()
        if not visible:
            self.setVisible(True)
        self.showMessage(title, body)
        if not visible:
            self.setVisible(False)
