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
        if (QSettings().value(GEOMETRY_KEY)):
            self.restoreGeometry(QSettings().value(GEOMETRY_KEY))
        else:
            self.resize(500, 500)
        if (QSettings().value(STATE_KEY)):
            self.showMaximized()

        self.setMicaEffectEnabled(False)

    def closeEvent(self, event):
        """Saves the current window geometry before closing."""
        QSettings().setValue(GEOMETRY_KEY, self.saveGeometry())
        if self.isMaximized():
            QSettings().setValue(STATE_KEY, True)
        else:
            QSettings().setValue(STATE_KEY, None)
        event.accept()
