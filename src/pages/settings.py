from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
import qfluentwidgets
from qfluentwidgets import (
    ComboBoxSettingCard,
    ColorSettingCard,
    PrimaryToolButton,
    FluentIcon,
    FlowLayout,
    SingleDirectionScrollArea,
    Dialog
)

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
               if theme.value != qfluentwidgets.Theme.AUTO.value else "Automatic"
               for theme in qfluentwidgets.Theme
            ]
        )
        comboBox.setMaximumWidth(500)

        colorPicker = ColorSettingCard(
            config.color,
            FluentIcon.PALETTE,
            "Color",
            "Change the primary color of the app.",
        )
        colorPicker.setMaximumWidth(500)

        settingsLayout = FlowLayout()
        settingsLayout.addWidget(comboBox)
        settingsLayout.addWidget(colorPicker)


        dialog = Dialog(
            "Are you sure you want to reset all settings?",
            "Every value will return to its default if you proceed.",
        )
        dialog.setTitleBarVisible(False)
        dialog.yesButton.setText("Reset")
        dialog.cancelButton.setText("Cancel")

        reset = PrimaryToolButton(
            FluentIcon.HISTORY
        )
        reset.setFixedWidth(100)
        reset.clicked.connect(lambda: (config.reset() if dialog.exec() else None))

        resetLayout = QHBoxLayout()
        resetLayout.addWidget(reset)

        contentWidget = QWidget()
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        contentLayout.setContentsMargins(40, 40, 50, 40)
        contentLayout.setSpacing(40)
        contentLayout.addLayout(resetLayout)
        contentLayout.addLayout(settingsLayout)

        scrollArea = SingleDirectionScrollArea(orient=Qt.Orientation.Vertical)
        scrollArea.setWidget(contentWidget)
        scrollArea.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        scrollArea.setWidgetResizable(True)
        scrollArea.enableTransparentBackground()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(scrollArea)

        self.setLayout(mainLayout)
