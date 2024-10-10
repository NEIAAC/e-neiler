from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ComboBox

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Settings")
        comboBox = ComboBox()
        # comboBox.addItems(SUPPORTED_THEMES)
        # comboBox.setCurrentIndex(SUPPORTED_THEMES.index(App.getTheme()))
        # comboBox.activated.connect(lambda: App.setTheme(comboBox.currentText()))
        layout = QVBoxLayout()
        layout.addWidget(comboBox)
        self.setLayout(layout)
