from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PySide6.QtCore import Qt
from qfluentwidgets import LineEdit, PasswordLineEdit, TextBrowser, PrimaryToolButton, FluentIcon

DEFAULT_TEXT = "Use the button on the left to load a template of the email body!"

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Home")

        # SMTP host input
        smtpHostInput = LineEdit()
        smtpHostInput.setMaximumWidth(500)
        hostLabel = QLabel("SMTP HOST")

        smtpHostInputLayout = QVBoxLayout()
        smtpHostInputLayout.setSpacing(10)
        smtpHostInputLayout.addWidget(hostLabel)
        smtpHostInputLayout.addWidget(smtpHostInput)

        # SMTP password input
        smtpPasswordInput = PasswordLineEdit()
        smtpPasswordInput.setMaximumWidth(500)
        passwordLabel = QLabel("SMTP PASSWORD")

        smtpPasswordInputLayout = QVBoxLayout()
        smtpPasswordInputLayout.setSpacing(10)
        smtpPasswordInputLayout.addWidget(passwordLabel)
        smtpPasswordInputLayout.addWidget(smtpPasswordInput)

        # Create a new VBox for the SMTP input fields
        smtpInputLayout = QVBoxLayout()
        smtpInputLayout.setSpacing(20)
        smtpInputLayout.addLayout(smtpHostInputLayout)
        smtpInputLayout.addLayout(smtpPasswordInputLayout)

        # Body file dialog
        bodyFileDialog = QFileDialog()
        bodyFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        # Email body input (TextBrowser)
        emailBodyInput = TextBrowser()
        emailBodyInput.setReadOnly(True)
        emailBodyInput.setPlaceholderText(DEFAULT_TEXT)

        clearBodyButton = PrimaryToolButton(FluentIcon.DELETE)
        clearBodyButton.setDisabled(True)
        clearBodyButton.clicked.connect(lambda: (emailBodyInput.clear(), clearBodyButton.setDisabled(True)))

        def loadEmailBody(emailBodyInput, filePath):
            if filePath:
                with open(filePath, 'r', encoding='utf-8') as file:
                    fileContent = file.read()
                    if filePath.endswith('.html'):
                        emailBodyInput.setHtml(fileContent)
                    else:
                        emailBodyInput.setText(fileContent)
                    clearBodyButton.setDisabled(False)

        selectBodyButton = PrimaryToolButton(FluentIcon.FOLDER)
        selectBodyButton.clicked.connect(lambda: loadEmailBody(emailBodyInput, bodyFileDialog.getOpenFileName()[0]))

        # Create horizontal layout for buttons and email body
        emailReaderLayout = QHBoxLayout()
        emailReaderLayout.setSpacing(10)
        buttonLayout = QVBoxLayout()
        buttonLayout.setSpacing(10)

        # Add buttons to buttonLayout
        buttonLayout.addWidget(selectBodyButton)
        buttonLayout.addWidget(clearBodyButton)

        # Align the buttons to the top of the buttonLayout
        buttonLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add button layout (left) and emailBodyInput (right) to bodyLayout
        emailReaderLayout.addLayout(buttonLayout)
        emailReaderLayout.addWidget(emailBodyInput)

        # submit button
        startButton = PrimaryToolButton(FluentIcon.PLAY)
        startButton.setFixedWidth(100)

        startButtonLayout = QHBoxLayout()
        startButtonLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        startButtonLayout.addWidget(startButton)

        # Main layout for the entire page
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        mainLayout.setContentsMargins(40, 40, 40, 40)
        mainLayout.setSpacing(40)

        mainLayout.addLayout(smtpInputLayout)
        mainLayout.addLayout(emailReaderLayout)  # Add the horizontal layout for buttons and text
        mainLayout.addLayout(startButtonLayout)

        # Set the main layout
        self.setLayout(mainLayout)
