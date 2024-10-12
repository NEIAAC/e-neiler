import logging

from PySide6.QtCore import QLocale
from qfluentwidgets import QConfig, EnumSerializer, OptionsConfigItem, OptionsValidator, ColorValidator, ColorSerializer
import qfluentwidgets

class Options(QConfig):
    """Global object for app options."""

    country = OptionsConfigItem("App", "locale", QLocale.Country.UnitedStates,
                               OptionsValidator(QLocale.Country), EnumSerializer(QLocale.Country), restart=True)

    language = OptionsConfigItem("App", "language", QLocale.Language.English,
                                OptionsValidator(QLocale.Language), EnumSerializer(QLocale.Language), restart=True)
    themeMode = OptionsConfigItem("Window", "theme", qfluentwidgets.Theme.DARK,
                                OptionsValidator(qfluentwidgets.Theme), EnumSerializer(qfluentwidgets.Theme))
    themeColor = OptionsConfigItem("Window", "themeColor", "#2BA9ED",
                                   ColorValidator(qfluentwidgets.QColor()), ColorSerializer())
customizable = Options()
customizable.themeMode.valueChanged.connect(lambda theme: (qfluentwidgets.setTheme(theme),
                                                       logging.info(f"Theme mode set to {theme.value}")))
customizable.themeColor.valueChanged.connect(lambda color: (qfluentwidgets.setThemeColor(color),
                                                       logging.info(f"Theme color set to {color}")))
