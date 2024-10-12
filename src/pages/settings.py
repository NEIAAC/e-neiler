from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
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
        comboBox.setMaximumWidth(500)

        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        mainLayout.setContentsMargins(40, 40, 40, 40)
        mainLayout.setSpacing(40)

        mainLayout.addWidget(comboBox)

        self.setLayout(mainLayout)
