import os
import sys

from PySide6.QtCore import QSize, QPoint
try:
    old = sys.stdout
    sys.stdout = open(os.devnull, "w")
    from qfluentwidgets import FluentWindow, FluentIcon, NavigationItemPosition
finally:
    sys.stdout.close()
    sys.stdout = old

from utils.config import config

from pages.home import HomePage
from pages.settings import SettingsPage

class Window(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setMicaEffectEnabled(False)
        self.resize(QSize(config.width.value, config.height.value))
        self.move(QPoint(config.x.value, config.y.value))
        if config.maximized.value:
            self.showMaximized()

        self.addSubInterface(HomePage(), FluentIcon.HOME, "Home")
        self.addSubInterface(SettingsPage(), FluentIcon.SETTING, "Settings", NavigationItemPosition.BOTTOM)

    def closeEvent(self, event):
        """Saves the current window geometry before closing."""
        config.width.value = self.width()
        config.height.value = self.height()
        config.x.value = self.x()
        config.y.value = self.y()
        config.maximized.value = self.isMaximized()
        config.save()
        super().closeEvent(event)
