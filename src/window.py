import os
import sys

try:
    old = sys.stdout
    sys.stdout = open(os.devnull, "w")
    import qfluentwidgets
    from qfluentwidgets import (
        FluentWindow,
        FluentIcon,
        NavigationItemPosition,
        SplashScreen,
    )
finally:
    sys.stdout.close()
    sys.stdout = old
from PySide6.QtCore import QSize, QPoint

from utils.config import config
from pages.home import HomePage
from pages.settings import SettingsPage


class Window(FluentWindow):
    def __init__(self):
        super().__init__()

        self.setMicaEffectEnabled(False)
        self.resize(QSize(config.width.get(), config.height.get()))
        self.move(QPoint(config.x.get(), config.y.get()))
        if config.maximized.get():
            self.showMaximized()

        qfluentwidgets.setTheme(config.style.get())
        qfluentwidgets.setThemeColor(config.color.get())

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(128, 128))
        self.show()

        self.addSubInterface(HomePage(), FluentIcon.HOME, "Home")
        self.addSubInterface(
            SettingsPage(),
            FluentIcon.SETTING,
            "Settings",
            NavigationItemPosition.BOTTOM,
        )

        self.splashScreen.finish()

    def closeEvent(self, event):
        """Saves the current window geometry before closing."""
        config.width.set(self.width())
        config.height.set(self.height())
        config.x.set(self.x())
        config.y.set(self.y())
        config.maximized.set(self.isMaximized())
        config.save()
        super().closeEvent(event)
