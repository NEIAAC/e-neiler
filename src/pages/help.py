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

        helpText = BodyLabel(
            f"""
            <h1>Help</h1>

            <p>
                <a href="https://github.com/FluentDesigns/qfluentwidgets">qfluentwidgets</a>
                is a lightweight, cross-platform, and cross-platform
                <a href="https://github.com/FluentDesigns/qfluentwidgets">QWidgets</a>
                for Windows, macOS, and Linux.
            </p>

           """,
        )

        contentWidget = QWidget()
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        contentLayout.setContentsMargins(40, 40, 50, 40)
        contentLayout.setSpacing(40)
        contentLayout.addWidget(helpText)

        scrollArea = SingleDirectionScrollArea(orient=Qt.Orientation.Vertical)
        scrollArea.setWidget(contentWidget)
        scrollArea.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        scrollArea.setWidgetResizable(True)
        scrollArea.enableTransparentBackground()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(scrollArea)

        self.setLayout(mainLayout)
