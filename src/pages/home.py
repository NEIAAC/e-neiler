import os
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QSizePolicy,
)
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import Qt, QUrl
from qfluentwidgets import (
    LineEdit,
    PasswordLineEdit,
    BodyLabel,
    PrimaryToolButton,
    FluentIcon,
    SmoothMode,
    SingleDirectionScrollArea,
    TextBrowser,
    InfoBar,
    InfoBarPosition,
    SpinBox,
)

from app import App
from services.email import EmailerThread
from utils.data_saver import config
from utils import file_loader
from utils.logger import LogLevel


class HomePage(QWidget):
    worker: EmailerThread | None = None

    def __init__(self):
        super().__init__()
        self.setObjectName("Home")

        self.finishSound = QSoundEffect()
        self.finishSound.setSource(
            QUrl.fromLocalFile(
                file_loader.getResourcePath(
                    os.path.join("sounds", "success.wav")
                )
            )
        )
        self.finishSound.setVolume(0.1)

        self.smtphostLabel = BodyLabel("<b>SMTP HOST</b>")
        self.smtpHostInput = LineEdit()
        self.smtpHostInput.setMaximumWidth(500)
        self.smtpHostInput.setText(config.smtpHost.get())
        self.smtpHostInput.setPlaceholderText("smtp.gmail.com")
        self.smtpHostInput.textChanged.connect(
            lambda text: config.smtpHost.set(text)
        )
        self.smtpHostInputLayout = QVBoxLayout()
        self.smtpHostInputLayout.setSpacing(10)
        self.smtpHostInputLayout.addWidget(self.smtphostLabel)
        self.smtpHostInputLayout.addWidget(self.smtpHostInput)

        self.smtpPortLabel = BodyLabel("<b>SMTP PORT</b>")
        self.smtpPortInput = LineEdit()
        self.smtpPortInput.setMaximumWidth(500)
        self.smtpPortInput.setText(config.smtpPort.get())
        self.smtpPortInput.textChanged.connect(
            lambda text: config.smtpPort.set(text)
        )
        self.smtpPortInputLayout = QVBoxLayout()
        self.smtpPortInputLayout.setSpacing(10)
        self.smtpPortInputLayout.addWidget(self.smtpPortLabel)
        self.smtpPortInputLayout.addWidget(self.smtpPortInput)

        self.smtpServerLayout = QHBoxLayout()
        self.smtpServerLayout.addLayout(self.smtpHostInputLayout)
        self.smtpServerLayout.addLayout(self.smtpPortInputLayout)

        self.smtpUsernameLabel = BodyLabel("<b>SMTP USERNAME</b>")
        self.smtpUsernameInput = LineEdit()
        self.smtpUsernameInput.setMaximumWidth(500)
        self.smtpUsernameInput.setText(config.smtpUsername.get())
        self.smtpUsernameInput.setPlaceholderText("person@example.com")
        self.smtpUsernameInput.textChanged.connect(
            lambda text: config.smtpUsername.set(text)
        )
        self.smtpUsernameLayout = QVBoxLayout()
        self.smtpUsernameLayout.setSpacing(10)
        self.smtpUsernameLayout.addWidget(self.smtpUsernameLabel)
        self.smtpUsernameLayout.addWidget(self.smtpUsernameInput)

        self.smtpPasswordLabel = BodyLabel("<b>SMTP PASSWORD</b>")
        self.smtpPasswordInput = PasswordLineEdit()
        self.smtpPasswordInput.setText(config.smtpPassword.get())
        self.smtpPasswordInput.setMaximumWidth(500)
        self.smtpPasswordInput.textChanged.connect(
            lambda text: config.smtpPassword.set(text)
        )
        self.smtpPasswordLayout = QVBoxLayout()
        self.smtpPasswordLayout.setSpacing(10)
        self.smtpPasswordLayout.addWidget(self.smtpPasswordLabel)
        self.smtpPasswordLayout.addWidget(self.smtpPasswordInput)

        self.smtpAuthLayout = QHBoxLayout()
        self.smtpAuthLayout.addLayout(self.smtpUsernameLayout)
        self.smtpAuthLayout.addLayout(self.smtpPasswordLayout)

        self.smtpDelayLabel = BodyLabel("<b>SMTP DELAY</b>")
        self.smtpDelayInput = SpinBox()
        self.smtpDelayInput.setFixedWidth(200)
        self.smtpDelayInput.setMinimum(1)
        self.smtpDelayInput.setValue(config.smtpDelay.get())
        self.smtpDelayInput.textChanged.connect(
            lambda text: config.smtpDelay.set(float(text))
        )

        self.smtpDelayLayout = QVBoxLayout()
        self.smtpDelayLayout.setSpacing(10)
        self.smtpDelayLayout.addWidget(self.smtpDelayLabel)
        self.smtpDelayLayout.addWidget(self.smtpDelayInput)

        self.smtpExtrasLayout = QHBoxLayout()
        self.smtpExtrasLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.smtpExtrasLayout.addLayout(self.smtpDelayLayout)

        self.smtpLayout = QVBoxLayout()
        self.smtpLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.smtpLayout.setSpacing(20)
        self.smtpLayout.addLayout(self.smtpServerLayout)
        self.smtpLayout.addLayout(self.smtpAuthLayout)
        self.smtpLayout.addLayout(self.smtpExtrasLayout)

        self.subjectLabel = BodyLabel("<b>SUBJECT</b>")
        self.subjectInput = LineEdit()
        self.subjectInput.setPlaceholderText(
            "The title of the email goes here."
        )
        self.subjectInput.setMaximumWidth(500)

        self.fromLabel = BodyLabel("<b>FROM</b>")
        self.fromInput = LineEdit()
        self.fromInput.setMaximumWidth(500)
        self.fromInput.setText(config.origin.get())
        self.fromInput.textChanged.connect(lambda text: config.origin.set(text))

        self.replyLabel = BodyLabel("<b>REPLY</b>")
        self.replyInput = LineEdit()
        self.replyInput.setMaximumWidth(500)
        self.replyInput.setText(config.reply.get())
        self.replyInput.textChanged.connect(lambda text: config.reply.set(text))

        self.ccLabel = BodyLabel("<b>CC</b>")
        self.ccInput = LineEdit()
        self.ccInput.setMaximumWidth(500)

        self.bccLabel = BodyLabel("<b>BCC</b>")
        self.bccInput = LineEdit()
        self.bccInput.setMaximumWidth(500)

        self.headLayout = QVBoxLayout()
        self.headLayout.setSpacing(10)
        self.headLayout.addWidget(self.subjectLabel)
        self.headLayout.addWidget(self.subjectInput)
        self.headLayout.addWidget(self.fromLabel)
        self.headLayout.addWidget(self.fromInput)
        self.headLayout.addWidget(self.replyLabel)
        self.headLayout.addWidget(self.replyInput)
        self.headLayout.addWidget(self.ccLabel)
        self.headLayout.addWidget(self.ccInput)
        self.headLayout.addWidget(self.bccLabel)
        self.headLayout.addWidget(self.bccInput)

        self.templateLabel = BodyLabel("<b>BODY TEMPLATE FILE</b>")
        self.templatePicker = QFileDialog()
        self.templatePicker.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.templateFileInput = LineEdit()
        self.templateFileInput.setMaximumWidth(500)
        self.templateFileInput.setReadOnly(True)
        self.templateFileInput.setPlaceholderText(
            "No body template file selected."
        )
        self.templateFileDialog = QFileDialog()
        self.templateFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.templateFilePickButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.templateFilePickButton.clicked.connect(
            lambda: self.templateFileInput.setText(
                self.templateFileDialog.getOpenFileName(
                    self, "Select a body template file!"
                )[0]
            )
        )
        self.templateContentLayout = QHBoxLayout()
        self.templateContentLayout.setSpacing(10)
        self.templateContentLayout.addWidget(self.templateFilePickButton)
        self.templateContentLayout.addWidget(self.templateFileInput)
        self.templateLayout = QVBoxLayout()
        self.templateLayout.setSpacing(10)
        self.templateLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.templateLayout.addWidget(self.templateLabel)
        self.templateLayout.addLayout(self.templateContentLayout)

        self.tableLabel = BodyLabel("<b>VARIABLE TABLE FILE</b>")
        self.tableFileInput = LineEdit()
        self.tableFileInput.setReadOnly(True)
        self.tableFileInput.setMaximumWidth(500)
        self.tableFileInput.setPlaceholderText("No table file selected.")
        self.tableFileDialog = QFileDialog()
        self.tableFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.tableFilePickButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.tableFilePickButton.clicked.connect(
            lambda: self.tableFileInput.setText(
                self.tableFileDialog.getOpenFileName(
                    self, "Select a table file!"
                )[0]
            )
        )
        self.tableContentLayout = QHBoxLayout()
        self.tableContentLayout.setSpacing(10)
        self.tableContentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tableContentLayout.addWidget(self.tableFilePickButton)
        self.tableContentLayout.addWidget(self.tableFileInput)
        self.tableLayout = QVBoxLayout()
        self.tableLayout.setSpacing(10)
        self.tableLayout.addWidget(self.tableLabel)
        self.tableLayout.addLayout(self.tableContentLayout)

        self.attachmentLabel = BodyLabel("<b>ATTACHMENTS DIRECTORY</b>")
        self.attachmentFolderInput = LineEdit()
        self.attachmentFolderInput.setReadOnly(True)
        self.attachmentFolderInput.setMaximumWidth(500)
        self.attachmentFolderInput.setPlaceholderText(
            "No attachment folder selected."
        )
        self.attachmentFileDialog = QFileDialog()
        self.attachmentFileDialog.setFileMode(QFileDialog.FileMode.Directory)
        self.attachmentFolderPickButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.attachmentFolderPickButton.clicked.connect(
            lambda: self.attachmentFolderInput.setText(
                self.attachmentFileDialog.getExistingDirectory(
                    self, "Select the directory to load table attachments from!"
                )
            )
        )
        self.attachmentContentLayout = QHBoxLayout()
        self.attachmentContentLayout.setSpacing(10)
        self.attachmentContentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.attachmentContentLayout.addWidget(self.attachmentFolderPickButton)
        self.attachmentContentLayout.addWidget(self.attachmentFolderInput)
        self.attachmentLayout = QVBoxLayout()
        self.attachmentLayout.setSpacing(10)
        self.attachmentLayout.addWidget(self.attachmentLabel)
        self.attachmentLayout.addLayout(self.attachmentContentLayout)

        self.runLogsBox = TextBrowser()
        self.runLogsBox.setHtml("")
        self.runLogsBox.setMinimumHeight(150)
        self.runLogsBox.setMaximumHeight(300)
        self.runLogsBox.setReadOnly(True)
        self.runLogsBox.setPlaceholderText(
            "Press the start button on the left to begin. \
            \nLog output from the run will be shown here. \
            \nThe trash can button will clear this box."
        )
        self.runButton = PrimaryToolButton(FluentIcon.PLAY)
        self.runButton.setFixedWidth(100)
        self.runButton.clicked.connect(self.runEmailer)
        self.runLogsClearButton = PrimaryToolButton(FluentIcon.DELETE)
        self.runLogsClearButton.setDisabled(True)
        self.runLogsClearButton.setFixedWidth(100)
        self.runLogsClearButton.clicked.connect(
            lambda: (
                self.runLogsBox.clear(),  # type: ignore
                self.runLogsClearButton.setDisabled(True),
            )
        )
        self.runButtonLayout = QVBoxLayout()
        self.runButtonLayout.setSpacing(10)
        self.runButtonLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.runButtonLayout.addWidget(self.runButton)
        self.runButtonLayout.addWidget(self.runLogsClearButton)
        self.runContentLayout = QHBoxLayout()
        self.runContentLayout.setSpacing(10)
        self.runContentLayout.addLayout(self.runButtonLayout)
        self.runContentLayout.addWidget(self.runLogsBox)

        self.contentLayout = QVBoxLayout()
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.contentLayout.setContentsMargins(40, 40, 50, 40)
        self.contentLayout.setSpacing(40)
        self.contentLayout.addLayout(self.smtpLayout)
        self.contentLayout.addLayout(self.headLayout)
        self.contentLayout.addLayout(self.templateLayout)
        self.contentLayout.addLayout(self.tableLayout)
        self.contentLayout.addLayout(self.attachmentLayout)
        self.contentLayout.addLayout(self.runContentLayout)
        self.contentWidget = QWidget()
        self.contentWidget.setLayout(self.contentLayout)

        self.scrollArea = SingleDirectionScrollArea(
            orient=Qt.Orientation.Vertical
        )
        self.scrollArea.setWidget(self.contentWidget)
        self.scrollArea.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.enableTransparentBackground()
        self.scrollArea.setSmoothMode(SmoothMode.NO_SMOOTH)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scrollArea)

        self.setLayout(self.mainLayout)

    def runEmailer(self):
        """Runs the emailer logic for this page."""

        if self.worker is not None and self.worker.isRunning():
            return

        schema = {
            "SMTP Host": self.smtpHostInput.text(),
            "SMTP Port": self.smtpPortInput.text(),
            "SMTP Username": self.smtpUsernameInput.text(),
            "SMTP Password": self.smtpPasswordInput.text(),
            "SMTP Delay": self.smtpDelayInput.text(),
            "Subject": self.subjectInput.text(),
            "Variable Table file": self.tableFileInput.text(),
            "Attachment folder": self.attachmentFolderInput.text(),
            "Body Template file": self.templateFileInput.text(),
        }

        # Make From field mandatory only if we can't build it from the username ourselves
        if "@" not in self.smtpUsernameInput.text():
            schema["From"] = self.fromInput.text()

        for input in schema:
            if schema[input] is None or schema[input] == "":
                InfoBar.error(
                    title=f"{input} field cannot be empty!",
                    content="",
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=4000,
                    parent=self,
                )
                return

        self.runButton.setDisabled(True)

        self.worker = EmailerThread(
            self.smtpHostInput.text(),
            self.smtpPortInput.text(),
            self.smtpUsernameInput.text(),
            self.smtpPasswordInput.text(),
            self.smtpDelayInput.value(),
            self.subjectInput.text(),
            self.fromInput.text()
            if self.fromInput.text()
            else self.smtpUsernameInput.text(),
            self.replyInput.text(),
            self.ccInput.text(),
            self.bccInput.text(),
            self.templateFileInput.text(),
            self.tableFileInput.text(),
            self.attachmentFolderInput.text(),
        )

        def output(text: str, level: LogLevel):
            if level == LogLevel.ERROR.value:
                self.runLogsBox.append(f'<font color="red">{text}</font>')
            elif level == LogLevel.WARNING.value:
                self.runLogsBox.append(f'<font color="olive">{text}</font>')
            elif level == LogLevel.SUCCESS.value:
                self.runLogsBox.append(f'<font color="green">{text}</font>')
            else:
                self.runLogsBox.append(f'<font color="gray">{text}</font>')
            self.runLogsClearButton.setDisabled(False)

        self.worker.outputSignal.connect(output)

        def finished():
            self.runButton.setDisabled(False)
            App.alert(self, 0)
            self.finishSound.play()

        self.worker.finished.connect(finished)
        self.worker.start()
