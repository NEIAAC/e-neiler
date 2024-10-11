from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog
from qfluentwidgets import LineEdit, PasswordLineEdit, TextBrowser, PushButton

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Home")
        layout = QVBoxLayout()

        smtpHostInput = LineEdit()
        hostLabel = QLabel("SMTP Host:")

        smtpPasswordInput = PasswordLineEdit()
        passwordLabel = QLabel("SMTP Password:")

        bodyFileDialog = QFileDialog()
        bodyFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        emailBodyInput = TextBrowser()

        selectBodyButton = PushButton("Select Email Body")
        selectBodyButton.clicked.connect(lambda: self.loadEmailBody(emailBodyInput, bodyFileDialog.getOpenFileName()[0]))

        layout.addWidget(hostLabel)
        layout.addWidget(smtpHostInput)
        layout.addWidget(passwordLabel)
        layout.addWidget(smtpPasswordInput)
        layout.addWidget(selectBodyButton)
        layout.addWidget(emailBodyInput)

        self.setLayout(layout)

    def loadEmailBody(self, emailBodyInput, filePath):
        if filePath:
            with open(filePath, 'r', encoding='utf-8') as file:
                fileContent = file.read()
                if filePath.endswith('.html'):
                    emailBodyInput.setHtml(fileContent)
                else:
                    emailBodyInput.setText(fileContent)
