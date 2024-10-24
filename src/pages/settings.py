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
    Dialog,
)

from utils.config import config


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Settings")

        self.comboBox = ComboBoxSettingCard(
            config.style,
            FluentIcon.BRUSH,
            "Theme",
            "Change the theme mode of the app.",
            texts=[
                theme.value
                if theme.value != qfluentwidgets.Theme.AUTO.value
                else "Automatic"
                for theme in qfluentwidgets.Theme
            ],
        )
        self.comboBox.setMaximumWidth(500)
        config.style.valueChanged.connect(
            lambda mode: (qfluentwidgets.setTheme(mode))
        )

        self.colorPicker = ColorSettingCard(
            config.color,
            FluentIcon.PALETTE,
            "Color",
            "Change the primary color of the app.",
        )
        self.colorPicker.setMaximumWidth(500)
        config.color.valueChanged.connect(
            lambda color: (qfluentwidgets.setThemeColor(color))
        )

        self.settingsLayout = FlowLayout()
        self.settingsLayout.addWidget(self.comboBox)
        self.settingsLayout.addWidget(self.colorPicker)

        self.dialog = Dialog(
            "Are you sure you want to reset all settings?",
            "Every value will return to its default if you proceed.",
        )
        self.dialog.setTitleBarVisible(False)
        self.dialog.yesButton.setText("Reset")
        self.dialog.cancelButton.setText("Cancel")

        self.reset = PrimaryToolButton(FluentIcon.DELETE)
        self.reset.setFixedWidth(100)
        self.reset.clicked.connect(
            lambda: (config.reset() if self.dialog.exec() else None)
        )

        self.resetLayout = QHBoxLayout()
        self.resetLayout.addWidget(self.reset)

        self.contentWidget = QWidget()
        self.contentLayout = QVBoxLayout(self.contentWidget)
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.contentLayout.setContentsMargins(40, 40, 50, 40)
        self.contentLayout.setSpacing(40)
        self.contentLayout.addLayout(self.resetLayout)
        self.contentLayout.addLayout(self.settingsLayout)

        self.scrollArea = SingleDirectionScrollArea(
            orient=Qt.Orientation.Vertical
        )
        self.scrollArea.setWidget(self.contentWidget)
        self.scrollArea.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.enableTransparentBackground()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scrollArea)

        self.setLayout(self.mainLayout)
