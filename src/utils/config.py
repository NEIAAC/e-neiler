import os

import qfluentwidgets
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

from utils.constants import DATA_PATH

CONFIG_PATH = os.path.join(DATA_PATH, "config.json")


class ConfigItem(OptionsConfigItem):
    def set(self, value, save=False):
        self.value = value
        if save:
            self.parent.save()

    def get(self):
        return self.value


class Config(QConfig):
    """Global object for app data."""

    maximized = ConfigItem("Window", "Maximized", False, BoolValidator())
    width = ConfigItem("Window", "Width", 500)
    height = ConfigItem("Window", "Height", 500)
    x = ConfigItem("Window", "X", 0)
    y = ConfigItem("Window", "Y", 0)
    style = ConfigItem(
        "Window",
        "Style",
        qfluentwidgets.Theme.DARK,
        OptionsValidator(qfluentwidgets.Theme),
        EnumSerializer(qfluentwidgets.Theme),
    )
    color = ConfigItem(
        "Window",
        "Color",
        qfluentwidgets.QColor("#4DA8DF"),
        ColorValidator(qfluentwidgets.QColor()),
        ColorSerializer(),
    )

    smtpHost = ConfigItem("Email", "SMTPHost", "")
    smtpPort = ConfigItem("Email", "SMTPPort", "587")
    smtpUsername = ConfigItem("Email", "SMTPUsername", "")
    smtpPassword = ConfigItem("Email", "SMTPPassword", "")
    origin = ConfigItem("Email", "Origin", "")

    def reset(self):
        for _, attr in self.__class__.__dict__.items():
            if isinstance(attr, ConfigItem):
                attr.set(attr.defaultValue)


config = Config()

qconfig.load(CONFIG_PATH, config)
