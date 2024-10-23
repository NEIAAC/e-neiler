from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from qfluentwidgets import (
    BodyLabel,
    SingleDirectionScrollArea,
)


class HelpPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Help")

        self.helpText = BodyLabel(
            """
            <h1>Help</h1>

            <p>
                <a href="https://github.com/FluentDesigns/qfluentwidgets">qfluentwidgets</a>
                is a lightweight, cross-platform, and cross-platform
                <a href="https://github.com/FluentDesigns/qfluentwidgets">QWidgets</a>
                for Windows, macOS, and Linux.
            </p>

           """,
        )

        self.contentWidget = QWidget()
        self.contentLayout = QVBoxLayout(self.contentWidget)
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.contentLayout.setContentsMargins(40, 40, 50, 40)
        self.contentLayout.setSpacing(40)
        self.contentLayout.addWidget(self.helpText)

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
