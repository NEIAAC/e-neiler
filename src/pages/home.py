from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QSizePolicy
from PySide6.QtCore import Qt
from qfluentwidgets import (
    LineEdit,
    PasswordLineEdit,
    TextEdit,
    PrimaryToolButton,
    FluentIcon,
    SingleDirectionScrollArea,
    PlainTextEdit
)

from logic.email import EmailerThread
from utils.config import config

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Home")

        smtpHostInput = LineEdit()
        smtpHostInput.setMaximumWidth(500)
        smtpHostInput.setText(config.smtpHost.get())
        smtpHostInput.setPlaceholderText("smtp.gmail.com")
        smtpHostInput.textChanged.connect(lambda text: config.smtpHost.set(text))
        smtphostLabel = QLabel("SMTP HOST")

        smtpPortInput = LineEdit()
        smtpPortInput.setMaximumWidth(500)
        smtpPortInput.setText(config.smtpPort.get())
        smtpHostInput.textChanged.connect(lambda text: config.smtpPort.set(text))
        smtpPortLabel = QLabel("SMTP PORT")

        smtpHostInputLayout = QVBoxLayout()
        smtpHostInputLayout.setSpacing(10)
        smtpHostInputLayout.addWidget(smtphostLabel)
        smtpHostInputLayout.addWidget(smtpHostInput)

        smtpPortInputLayout = QVBoxLayout()
        smtpPortInputLayout.setSpacing(10)
        smtpPortInputLayout.addWidget(smtpPortLabel)
        smtpPortInputLayout.addWidget(smtpPortInput)

        smtpServerLayout = QHBoxLayout()
        smtpServerLayout.addLayout(smtpHostInputLayout)
        smtpServerLayout.addLayout(smtpPortInputLayout)

        smtpUsernameInput = LineEdit()
        smtpUsernameInput.setMaximumWidth(500)
        smtpUsernameInput.setText(config.smtpUsername.get())
        smtpUsernameInput.setPlaceholderText("person@example.com")
        smtpUsernameInput.textChanged.connect(lambda text: config.smtpUsername.set(text))
        smtpusernameLabel = QLabel("SMTP USERNAME")

        smtpUsernameLayout = QVBoxLayout()
        smtpUsernameLayout.setSpacing(10)
        smtpUsernameLayout.addWidget(smtpusernameLabel)
        smtpUsernameLayout.addWidget(smtpUsernameInput)

        smtpPasswordInput = PasswordLineEdit()
        smtpPasswordInput.setText(config.smtpPassword.get())
        smtpPasswordInput.setMaximumWidth(500)
        smtpPasswordInput.textChanged.connect(lambda text: config.smtpPassword.set(text))
        smtppasswordLabel = QLabel("SMTP PASSWORD")

        smtpPasswordLayout = QVBoxLayout()
        smtpPasswordLayout.setSpacing(10)
        smtpPasswordLayout.addWidget(smtppasswordLabel)
        smtpPasswordLayout.addWidget(smtpPasswordInput)

        smtpAuthLayout = QHBoxLayout()
        smtpAuthLayout.addLayout(smtpUsernameLayout)
        smtpAuthLayout.addLayout(smtpPasswordLayout)

        smtpLayout = QVBoxLayout()
        smtpLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        smtpLayout.setSpacing(20)
        smtpLayout.addLayout(smtpServerLayout)
        smtpLayout.addLayout(smtpAuthLayout)

        subjectInput = LineEdit()
        subjectInput.setMaximumWidth(500)
        subjectLabel = QLabel("SUBJECT")

        ccInput = LineEdit()
        ccInput.setMaximumWidth(500)
        ccInput.setPlaceholderText("Use a comma (,) to separate emails you want to CC!")
        ccLabel = QLabel("CC")

        bccInput = LineEdit()
        bccInput.setMaximumWidth(500)
        bccInput.setPlaceholderText("Use a comma (,) to separate emails you want to BCC!")
        bccLabel = QLabel("BCC")

        headLayout = QVBoxLayout()
        headLayout.setSpacing(10)
        headLayout.addWidget(subjectLabel)
        headLayout.addWidget(subjectInput)
        headLayout.addWidget(ccLabel)
        headLayout.addWidget(ccInput)
        headLayout.addWidget(bccLabel)
        headLayout.addWidget(bccInput)

        templatePicker = QFileDialog()
        templatePicker.setFileMode(QFileDialog.FileMode.ExistingFile)

        templateContentBox = TextEdit()
        templateContentBox.setMinimumHeight(150)
        templateContentBox.setReadOnly(True)
        templateContentBox.setPlaceholderText(
            "Use the button on the left to load a template for the email body and visualize it here...")

        clearTemplateButton = PrimaryToolButton(FluentIcon.DELETE)
        clearTemplateButton.setDisabled(True)
        clearTemplateButton.clicked.connect(lambda: (templateContentBox.clear(), clearTemplateButton.setDisabled(True)))

        def loadEmailBody(emailBodyInput, filePath):
            if filePath:
                with open(filePath, 'r', encoding='utf-8') as file:
                    fileContent = file.read()
                    if filePath.endswith('.html'):
                        emailBodyInput.setHtml(fileContent)
                    else:
                        emailBodyInput.setText(fileContent)
                    clearTemplateButton.setDisabled(False)

        templatePickerButton = PrimaryToolButton(FluentIcon.FOLDER)
        templatePickerButton.clicked.connect(lambda: loadEmailBody(templateContentBox, templatePicker.getOpenFileName()[0]))

        templateButtonsLayout = QVBoxLayout()
        templateButtonsLayout.setSpacing(10)
        templateButtonsLayout.addWidget(templatePickerButton)
        templateButtonsLayout.addWidget(clearTemplateButton)
        templateButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        templateLayout = QHBoxLayout()
        templateLayout.setSpacing(10)
        templateLayout.addLayout(templateButtonsLayout)
        templateLayout.addWidget(templateContentBox)

        outputBox = PlainTextEdit()
        outputBox.setMinimumHeight(150)
        outputBox.setReadOnly(True)
        outputBox.setDisabled(True)
        outputBox.setPlaceholderText("Progress will be shown here.")

        startButton = PrimaryToolButton(FluentIcon.PLAY)
        startButton.setFixedWidth(100)

        worker = EmailerThread(outputBox, "data")
        worker.finished.connect(lambda: startButton.setDisabled(False))

        startButtonLayout = QHBoxLayout()
        startButtonLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        startButtonLayout.addWidget(startButton)
        startButton.clicked.connect(lambda: (startButton.setDisabled(True), worker.start()))

        contentWidget = QWidget()
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        contentLayout.setContentsMargins(40, 40, 40, 40)
        contentLayout.setSpacing(40)
        contentLayout.addLayout(smtpLayout)
        contentLayout.addLayout(headLayout)
        contentLayout.addLayout(templateLayout)
        contentLayout.addWidget(outputBox)
        contentLayout.addLayout(startButtonLayout)

        scrollArea = SingleDirectionScrollArea(orient=Qt.Orientation.Vertical)
        scrollArea.setWidget(contentWidget)
        scrollArea.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        scrollArea.setWidgetResizable(True)
        scrollArea.enableTransparentBackground()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(scrollArea)

        self.setLayout(mainLayout)
