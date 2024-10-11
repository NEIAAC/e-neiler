from PySide6.QtCore import QSettings

from qfluentwidgets import FluentWindow, FluentIcon, NavigationItemPosition

from pages.home import HomePage
from pages.settings import SettingsPage

GEOMETRY_KEY = "window/geometry"
STATE_KEY = "window/maximized"

class Window(FluentWindow):
    def __init__(self):
        super().__init__()

        self.addSubInterface(HomePage(), FluentIcon.HOME, "Home")
        self.addSubInterface(SettingsPage(), FluentIcon.SETTING, "Settings", position=NavigationItemPosition.BOTTOM)

        self.restoreGeometry(QSettings().value(GEOMETRY_KEY))
        if (QSettings().value(STATE_KEY)):
            self.showMaximized()

    def closeEvent(self, event):
        """Saves the current window geometry before closing."""
        QSettings().setValue(GEOMETRY_KEY, self.saveGeometry())
        if self.isMaximized():
            QSettings().setValue(STATE_KEY, True)
        else:
            QSettings().setValue(STATE_KEY, None)
        event.accept()
