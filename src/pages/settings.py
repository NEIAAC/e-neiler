from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ComboBoxSettingCard, FluentIcon, Theme

from utils.config import customizable

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Settings")

        comboBox = ComboBoxSettingCard(
            customizable.themeMode,
            FluentIcon.BRUSH,
            "Theme",
            "Change the appearance of the app.",
            texts=[
               "Light",
               "Dark",
               "System"
            ]
        )

        layout = QVBoxLayout()
        layout.addWidget(comboBox)

        self.setLayout(layout)
