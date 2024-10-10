from PySide6.QtCore import QSettings
from qfluentwidgets import FluentWindow, FluentIcon

from app import App

from pages.home import HomePage
from pages.settings import SettingsPage

GEOMETRY_KEY = "window/geometry"

class Window(FluentWindow):
    def __init__(self):
        super().__init__()

        self.restoreGeometry(QSettings().value(GEOMETRY_KEY))

        self.addSubInterface(HomePage(), FluentIcon.HOME, "Home")
        self.addSubInterface(SettingsPage(), FluentIcon.SETTING, "Settings")

    def closeEvent(self, event):
        """Saves the current window geometry before closing."""
        QSettings().setValue(GEOMETRY_KEY, self.saveGeometry())
        event.accept()
