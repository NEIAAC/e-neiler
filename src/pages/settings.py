from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import ComboBoxSettingCard, ColorSettingCard, PrimaryToolButton, FluentIcon, FlowLayout, Dialog, Theme
import qfluentwidgets

from utils.config import config

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Settings")

        comboBox = ComboBoxSettingCard(
            config.style,
            FluentIcon.BRUSH,
            "Theme",
            "Change the theme mode of the app.",
            texts=[
               theme.value
               if theme.value != Theme.AUTO.value else "Automatic"
               for theme in Theme
            ]
        )
        comboBox.setMaximumWidth(500)
        config.style.valueChanged.connect(lambda theme: (qfluentwidgets.setTheme(theme)))

        colorPicker = ColorSettingCard(
            config.primaryColor,
            FluentIcon.PALETTE,
            "Color",
            "Change the primary color of the app.",
        )
        colorPicker.setMaximumWidth(500)
        config.primaryColor.valueChanged.connect(lambda color: (qfluentwidgets.setThemeColor(color)))

        settingsLayout = FlowLayout()
        settingsLayout.addWidget(comboBox)
        settingsLayout.addWidget(colorPicker)

        reset = PrimaryToolButton(
            FluentIcon.SYNC,
        )
        reset.setFixedWidth(100)
        reset.clicked.connect(lambda: config.reset())

        resetLayout = QHBoxLayout()
        resetLayout.addWidget(reset)

        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        mainLayout.setContentsMargins(40, 40, 40, 40)
        mainLayout.setSpacing(40)

        mainLayout.addLayout(resetLayout)
        mainLayout.addLayout(settingsLayout)

        self.setLayout(mainLayout)
