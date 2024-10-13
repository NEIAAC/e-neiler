import os

from PySide6.QtCore import QLocale, QStandardPaths
from qfluentwidgets import (
    qconfig,
    QConfig,
    EnumSerializer,
    OptionsConfigItem,
    OptionsValidator,
    BoolValidator,
    ColorSerializer,
    ColorValidator,
)
import qfluentwidgets

from app import DATA_PATH

APP_NAME = "E-neiler"
AUTHOR_NAME = "NEIAAC"

class Config(QConfig):
    """
    Global object for app options.

    ThemeMode and ThemeColor are already present from the base qfluentwidgets.Config class.
    """

    country = OptionsConfigItem("App", "Locale", QLocale.Country.UnitedStates,
                               OptionsValidator(QLocale.Country), EnumSerializer(QLocale.Country), restart=True)
    language = OptionsConfigItem("App", "Language", QLocale.Language.English,
                                OptionsValidator(QLocale.Language), EnumSerializer(QLocale.Language), restart=True)

    maximized = OptionsConfigItem("Window", "Maximized", False, BoolValidator())
    width = OptionsConfigItem("Window", "Width", 500)
    height = OptionsConfigItem("Window", "Height", 500)
    x = OptionsConfigItem("Window", "X", 0)
    y = OptionsConfigItem("Window", "Y", 0)

    style = OptionsConfigItem("Window", "Style", qfluentwidgets.Theme.LIGHT,
                              OptionsValidator(qfluentwidgets.Theme), EnumSerializer(qfluentwidgets.Theme), save=True)
    primaryColor = OptionsConfigItem("Window", "PrimaryColor", qfluentwidgets.QColor("#4DA8DF"),
                                     ColorValidator(qfluentwidgets.QColor()), ColorSerializer())

    def reset(self):
            for _, attr in self.__class__.__dict__.items():
                if isinstance(attr, OptionsConfigItem):
                    attr.value = attr.defaultValue

config = Config()
qconfig.load(os.path.join(DATA_PATH, "config.json"), config)
