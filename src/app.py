from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

from utils import path

LOGO_PATH = "resources/icons/logo.png"

THEME_KEY = "app/style"
LOCALE_KEY = "app/locale"

class App(QApplication):
    def __init__(self, argv: list[str]):
        super().__init__(argv)

        self.setApplicationName("E-neiler")
        self.setOrganizationName("NEIAAC")
        self.setOrganizationDomain("neiaac.com")
        self.setWindowIcon(QIcon(QPixmap(path.fromBase(LOGO_PATH))))
        self.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
