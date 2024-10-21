from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFileDialog,
    QSizePolicy,
)
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import Qt, QUrl
from qfluentwidgets import (
    LineEdit,
    PasswordLineEdit,
    TextEdit,
    PrimaryToolButton,
    FluentIcon,
    SingleDirectionScrollArea,
    PlainTextEdit,
    InfoBar,
    InfoBarPosition,
)

from app import App
from logic.email import EmailerThread
from utils.config import config
from utils import loader
from utils.system_tray import SystemTray
from utils.constants import SUPPORTED_TABLE_FORMATS


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Home")

        self.finishSound = QSoundEffect()
        self.finishSound.setSource(
            QUrl.fromLocalFile(loader.resources("sounds/success.wav"))
        )
        self.finishSound.setVolume(0.2)

        # SMTP settings
        self.smtpHostInput = LineEdit()
        self.smtpHostInput.setMaximumWidth(500)
        self.smtpHostInput.setText(config.smtpHost.get())
        self.smtpHostInput.setPlaceholderText("smtp.gmail.com")
        self.smtpHostInput.textChanged.connect(
            lambda text: config.smtpHost.set(text)
        )
        self.smtphostLabel = QLabel("SMTP HOST")

        self.smtpPortInput = LineEdit()
        self.smtpPortInput.setMaximumWidth(500)
        self.smtpPortInput.setText(config.smtpPort.get())
        self.smtpPortInput.textChanged.connect(
            lambda text: config.smtpPort.set(text)
        )
        self.smtpPortLabel = QLabel("SMTP PORT")

        self.smtpHostInputLayout = QVBoxLayout()
        self.smtpHostInputLayout.setSpacing(10)
        self.smtpHostInputLayout.addWidget(self.smtphostLabel)
        self.smtpHostInputLayout.addWidget(self.smtpHostInput)

        self.smtpPortInputLayout = QVBoxLayout()
        self.smtpPortInputLayout.setSpacing(10)
        self.smtpPortInputLayout.addWidget(self.smtpPortLabel)
        self.smtpPortInputLayout.addWidget(self.smtpPortInput)

        self.smtpServerLayout = QHBoxLayout()
        self.smtpServerLayout.addLayout(self.smtpHostInputLayout)
        self.smtpServerLayout.addLayout(self.smtpPortInputLayout)

        self.smtpUsernameInput = LineEdit()
        self.smtpUsernameInput.setMaximumWidth(500)
        self.smtpUsernameInput.setText(config.smtpUsername.get())
        self.smtpUsernameInput.setPlaceholderText("person@example.com")
        self.smtpUsernameInput.textChanged.connect(
            lambda text: config.smtpUsername.set(text)
        )
        self.smtpusernameLabel = QLabel("SMTP USERNAME")

        self.smtpUsernameLayout = QVBoxLayout()
        self.smtpUsernameLayout.setSpacing(10)
        self.smtpUsernameLayout.addWidget(self.smtpusernameLabel)
        self.smtpUsernameLayout.addWidget(self.smtpUsernameInput)

        self.smtpPasswordInput = PasswordLineEdit()
        self.smtpPasswordInput.setText(config.smtpPassword.get())
        self.smtpPasswordInput.setMaximumWidth(500)
        self.smtpPasswordInput.textChanged.connect(
            lambda text: config.smtpPassword.set(text)
        )
        self.smtppasswordLabel = QLabel("SMTP PASSWORD")

        self.smtpPasswordLayout = QVBoxLayout()
        self.smtpPasswordLayout.setSpacing(10)
        self.smtpPasswordLayout.addWidget(self.smtppasswordLabel)
        self.smtpPasswordLayout.addWidget(self.smtpPasswordInput)

        self.smtpAuthLayout = QHBoxLayout()
        self.smtpAuthLayout.addLayout(self.smtpUsernameLayout)
        self.smtpAuthLayout.addLayout(self.smtpPasswordLayout)

        self.smtpLayout = QVBoxLayout()
        self.smtpLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.smtpLayout.setSpacing(20)
        self.smtpLayout.addLayout(self.smtpServerLayout)
        self.smtpLayout.addLayout(self.smtpAuthLayout)

        # Email headers
        self.subjectInput = LineEdit()
        self.subjectInput.setMaximumWidth(500)
        self.subjectLabel = QLabel("SUBJECT")

        self.ccInput = LineEdit()
        self.ccInput.setMaximumWidth(500)
        self.ccInput.setPlaceholderText(
            "Use a comma (,) to separate emails you want to CC!"
        )
        self.ccLabel = QLabel("CC")

        self.bccInput = LineEdit()
        self.bccInput.setMaximumWidth(500)
        self.bccInput.setPlaceholderText(
            "Use a comma (,) to separate emails you want to BCC!"
        )
        self.bccLabel = QLabel("BCC")

        self.headLayout = QVBoxLayout()
        self.headLayout.setSpacing(10)
        self.headLayout.addWidget(self.subjectLabel)
        self.headLayout.addWidget(self.subjectInput)
        self.headLayout.addWidget(self.ccLabel)
        self.headLayout.addWidget(self.ccInput)
        self.headLayout.addWidget(self.bccLabel)
        self.headLayout.addWidget(self.bccInput)

        self.templatePicker = QFileDialog()
        self.templatePicker.setFileMode(QFileDialog.FileMode.ExistingFile)

        self.templateContentBox = TextEdit()
        self.templateContentBox.setMinimumHeight(150)
        self.templateContentBox.setReadOnly(True)
        self.templateContentBox.setPlaceholderText(
            "Use the button on the left to load a template for the email body and visualize it here..."
        )

        self.clearTemplateButton = PrimaryToolButton(FluentIcon.DELETE)
        self.clearTemplateButton.setDisabled(True)
        self.clearTemplateButton.clicked.connect(
            lambda: self.clearTemplate(
                self.templateContentBox, self.clearTemplateButton
            )
        )

        self.templatePickerButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.templatePickerButton.clicked.connect(
            lambda: self.loadEmailBody(
                self.templateContentBox,
                self.clearTemplateButton,
                self.templatePicker,
            )
        )

        self.templateButtonsLayout = QVBoxLayout()
        self.templateButtonsLayout.setSpacing(10)
        self.templateButtonsLayout.addWidget(self.templatePickerButton)
        self.templateButtonsLayout.addWidget(self.clearTemplateButton)
        self.templateButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.templateLayout = QHBoxLayout()
        self.templateLayout.setSpacing(10)
        self.templateLayout.addLayout(self.templateButtonsLayout)
        self.templateLayout.addWidget(self.templateContentBox)

        self.tableFilePathLabel = QLabel("No table file selected")
        self.tableFilePathLabel.setMaximumWidth(500)

        self.tableFilePickerButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.tableFilePickerButton.clicked.connect(
            lambda: self.selectFile(self.tableFilePathLabel)
        )

        self.clearTableButton = PrimaryToolButton(FluentIcon.DELETE)
        self.clearTableButton.setDisabled(True)
        self.clearTableButton.clicked.connect(
            lambda: self.clearSelectedFile(
                self.tableFilePathLabel, self.clearTableButton
            )
        )

        self.tablePickerLayout = QHBoxLayout()
        self.tablePickerLayout.setSpacing(10)
        self.tablePickerLayout.addWidget(self.tableFilePickerButton)
        self.tablePickerLayout.addWidget(self.tableFilePathLabel)

        self.tableLayout = QVBoxLayout()
        self.tableLayout.addLayout(self.tablePickerLayout)
        self.tableLayout.addWidget(self.clearTableButton)

        self.outputBox = PlainTextEdit()
        self.outputBox.setMinimumHeight(150)
        self.outputBox.setReadOnly(True)
        self.outputBox.setPlaceholderText("Progress will be shown here.")

        self.outputClearButton = PrimaryToolButton(FluentIcon.DELETE)
        self.outputClearButton.setDisabled(True)
        self.outputClearButton.clicked.connect(self.outputBox.clear)

        self.outputButtonLayout = QVBoxLayout()
        self.outputButtonLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.outputButtonLayout.setSpacing(10)
        self.outputButtonLayout.addWidget(self.outputClearButton)

        self.outputLayout = QHBoxLayout()
        self.outputLayout.setSpacing(10)
        self.outputLayout.addLayout(self.outputButtonLayout)
        self.outputLayout.addWidget(self.outputBox)

        self.startButton = PrimaryToolButton(FluentIcon.PLAY)
        self.startButton.setFixedWidth(100)

        self.worker = None
        self.startButtonLayout = QHBoxLayout()
        self.startButtonLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.startButtonLayout.addWidget(self.startButton)
        self.startButton.clicked.connect(self.runEmailer)

        self.contentWidget = QWidget()
        self.contentLayout = QVBoxLayout(self.contentWidget)
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.contentLayout.setContentsMargins(40, 40, 50, 40)
        self.contentLayout.setSpacing(40)
        self.contentLayout.addLayout(self.smtpLayout)
        self.contentLayout.addLayout(self.headLayout)
        self.contentLayout.addLayout(self.templateLayout)
        self.contentLayout.addLayout(self.tableLayout)
        self.contentLayout.addWidget(self.outputBox)
        self.contentLayout.addLayout(self.startButtonLayout)

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

    def loadEmailBody(
        self, templateContentBox, clearTemplateButton, templatePicker
    ):
        filePath, _ = templatePicker.getOpenFileName()
        if filePath:
            with open(filePath, "r", encoding="utf-8") as file:
                fileContent = file.read()
                if filePath.endswith(".html"):
                    templateContentBox.setHtml(fileContent)
                else:
                    templateContentBox.setText(fileContent)
                clearTemplateButton.setDisabled(False)

    def clearTemplate(self, templateContentBox, clearTemplateButton):
        templateContentBox.clear()
        clearTemplateButton.setDisabled(True)

    def selectFile(self, filePathLabel):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilters(SUPPORTED_TABLE_FORMATS)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                filePathLabel.setText(selected_files[0])

    def clearSelectedFile(self, filePathLabel, clearButton):
        filePathLabel.setText("No table file selected")
        clearButton.setDisabled(True)

    def runEmailer(self):
        """Runs the example logic for this page."""
        if self.worker is not None and self.worker.isRunning():
            return

        if not self.templateContentBox.toPlainText():
            InfoBar.error(
                title="Template is empty!",
                content="",
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=4000,
                parent=self,
            )
            return

        self.startButton.setDisabled(True)
        self.worker = EmailerThread(self.templateContentBox.toPlainText())
        self.worker.outputSignal.connect(
            lambda text: (
                self.outputBox.appendPlainText(text),
                self.outputClearButton.setDisabled(False),
            )
        )

        def finished():
            self.startButton.setDisabled(False)
            App.alert(self, 0)
            if (
                App.applicationState()
                == Qt.ApplicationState.ApplicationInactive
            ):
                SystemTray().send("Example finished!", "Go back to the app.")
            self.finishSound.play()

        self.worker.finished.connect(finished)
        self.worker.start()


#
