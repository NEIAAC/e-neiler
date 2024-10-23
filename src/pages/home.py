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
    SingleDirectionScrollArea,
    TextBrowser,
    InfoBar,
    InfoBarPosition,
)

from app import App
from logic.email import EmailerThread
from utils.config import config
from utils import loader
from utils.system_tray import SystemTray


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Home")

        self.finishSound = QSoundEffect()
        self.finishSound.setSource(
            QUrl.fromLocalFile(loader.resources("sounds/success.wav"))
        )
        self.finishSound.setVolume(0.1)

        self.smtpHostInput = LineEdit()
        self.smtpHostInput.setMaximumWidth(500)
        self.smtpHostInput.setText(config.smtpHost.get())
        self.smtpHostInput.setPlaceholderText("smtp.gmail.com")
        self.smtpHostInput.textChanged.connect(
            lambda text: config.smtpHost.set(text)
        )
        self.smtphostLabel = BodyLabel("SMTP HOST*")

        self.smtpPortInput = LineEdit()
        self.smtpPortInput.setMaximumWidth(500)
        self.smtpPortInput.setText(config.smtpPort.get())
        self.smtpPortInput.textChanged.connect(
            lambda text: config.smtpPort.set(text)
        )
        self.smtpPortLabel = BodyLabel("SMTP PORT*")

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
        self.smtpusernameLabel = BodyLabel("SMTP USERNAME*")

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
        self.smtppasswordLabel = BodyLabel("SMTP PASSWORD*")

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

        self.subjectLabel = BodyLabel("SUBJECT*")
        self.subjectInput = LineEdit()
        self.subjectInput.setPlaceholderText(
            "The title of the email goes here."
        )
        self.subjectInput.setMaximumWidth(500)

        self.ccInput = LineEdit()
        self.ccInput.setMaximumWidth(500)
        self.ccInput.setPlaceholderText(
            "Use a comma , to separate emails you want to CC!"
        )
        self.ccLabel = BodyLabel("CC")

        self.bccInput = LineEdit()
        self.bccInput.setMaximumWidth(500)
        self.bccInput.setPlaceholderText(
            "Use a comma , to separate emails you want to BCC!"
        )
        self.bccLabel = BodyLabel("BCC")

        self.headLayout = QVBoxLayout()
        self.headLayout.setSpacing(10)
        self.headLayout.addWidget(self.subjectLabel)
        self.headLayout.addWidget(self.subjectInput)
        self.headLayout.addWidget(self.ccLabel)
        self.headLayout.addWidget(self.ccInput)
        self.headLayout.addWidget(self.bccLabel)
        self.headLayout.addWidget(self.bccInput)

        self.templateLabel = BodyLabel("TEMPLATE FILE*")
        self.templatePicker = QFileDialog()
        self.templatePicker.setFileMode(QFileDialog.FileMode.ExistingFile)

        self.templateFileBox = LineEdit()
        self.templateFileBox.setMaximumWidth(500)
        self.templateFileBox.setReadOnly(True)
        self.templateFileBox.setPlaceholderText("No template file selected.")

        self.templateFilePickButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.templateFilePickButton.clicked.connect(self.pickTemplateFile)

        self.templateContentLayout = QHBoxLayout()
        self.templateContentLayout.setSpacing(10)
        self.templateContentLayout.addWidget(self.templateFilePickButton)
        self.templateContentLayout.addWidget(self.templateFileBox)

        self.templateLayout = QVBoxLayout()
        self.templateLayout.setSpacing(10)
        self.templateLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.templateLayout.addWidget(self.templateLabel)
        self.templateLayout.addLayout(self.templateContentLayout)

        self.tableLabel = BodyLabel("TABLE FILE*")
        self.tableFileInput = LineEdit()
        self.tableFileInput.setReadOnly(True)
        self.tableFileInput.setMaximumWidth(500)
        self.tableFileInput.setPlaceholderText("No table file selected.")

        self.tableFilePickButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.tableFilePickButton.clicked.connect(self.pickTableFile)

        self.tableContentLayout = QHBoxLayout()
        self.tableContentLayout.setSpacing(10)
        self.tableContentLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tableContentLayout.addWidget(self.tableFilePickButton)
        self.tableContentLayout.addWidget(self.tableFileInput)

        self.tableLayout = QVBoxLayout()
        self.tableLayout.setSpacing(10)
        self.tableLayout.addWidget(self.tableLabel)
        self.tableLayout.addLayout(self.tableContentLayout)

        self.attachmentLabel = BodyLabel("ATTACHMENTS DIRECTORY*")
        self.attachmentFolderInput = LineEdit()
        self.attachmentFolderInput.setReadOnly(True)
        self.attachmentFolderInput.setMaximumWidth(500)
        self.attachmentFolderInput.setPlaceholderText(
            "No attachment folder selected."
        )

        self.attachmentFolderPickButton = PrimaryToolButton(FluentIcon.FOLDER)
        self.attachmentFolderPickButton.clicked.connect(
            self.pickAttachmentFolder
        )
        self.attachmentContentLayout = QHBoxLayout()
        self.attachmentContentLayout.setSpacing(10)
        self.attachmentContentLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.attachmentContentLayout.addWidget(self.attachmentFolderPickButton)
        self.attachmentContentLayout.addWidget(self.attachmentFolderInput)

        self.attachmentLayout = QVBoxLayout()
        self.attachmentLayout.setSpacing(10)
        self.attachmentLayout.addWidget(self.attachmentLabel)
        self.attachmentLayout.addLayout(self.attachmentContentLayout)

        self.runLogsBox = TextBrowser()
        self.runLogsBox.setHtml("")
        self.runLogsBox.setMinimumHeight(150)
        self.runLogsBox.setReadOnly(True)
        self.runLogsBox.setPlaceholderText(
            "Press the button on the left to start.\nLog output from the run will be shown here."
        )

        self.worker = None
        self.runButton = PrimaryToolButton(FluentIcon.PLAY)
        self.runButton.setFixedWidth(100)
        self.runButton.clicked.connect(self.runEmailer)

        self.runLogsClearButton = PrimaryToolButton(FluentIcon.DELETE)
        self.runLogsClearButton.setDisabled(True)
        self.runLogsClearButton.setFixedWidth(100)
        self.runLogsClearButton.clicked.connect(
            lambda: (
                self.runLogsBox.clear(),
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

        self.contentWidget = QWidget()
        self.contentLayout = QVBoxLayout(self.contentWidget)
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.contentLayout.setContentsMargins(40, 40, 50, 40)
        self.contentLayout.setSpacing(40)
        self.contentLayout.addLayout(self.smtpLayout)
        self.contentLayout.addLayout(self.headLayout)
        self.contentLayout.addLayout(self.templateLayout)
        self.contentLayout.addLayout(self.tableLayout)
        self.contentLayout.addLayout(self.attachmentLayout)
        self.contentLayout.addLayout(self.runContentLayout)

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

    def pickTemplateFile(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.templateFileBox.setText(
            dialog.getOpenFileName(self, "Select a template file!")[0]
        )

    def pickTableFile(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.tableFileInput.setText(
            dialog.getOpenFileName(
                self, "Select a table file!", "", "Table (*.csv *.xlsx)"
            )[0]
        )

    def pickAttachmentFolder(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        self.attachmentFolderInput.setText(
            dialog.getExistingDirectory(
                self,
                "Select the directory to load table attachments from!",
            )
        )

    def runEmailer(self):
        if self.worker is not None and self.worker.isRunning():
            return

        schema = {
            "SMTP Host": self.smtpHostInput.text(),
            "SMTP Port": self.smtpPortInput.text(),
            "SMTP Username": self.smtpUsernameInput.text(),
            "SMTP Password": self.smtpPasswordInput.text(),
            "Subject": self.subjectInput.text(),
            "Table file": self.tableFileInput.text(),
            "Attachment folder": self.attachmentFolderInput.text(),
            "Template file": self.templateFileBox.text(),
        }
        for input in schema:
            if not schema[input]:
                InfoBar.error(
                    title=f"{input} field is empty!",
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
            self.subjectInput.text(),
            self.ccInput.text(),
            self.bccInput.text(),
            self.templateFileBox.text(),
            self.tableFileInput.text(),
            self.attachmentFolderInput.text(),
        )

        def output(text, level):
            if level == "ERROR":
                self.runLogsBox.append(f'<font color="red">{text}</font>')
            else:
                self.runLogsBox.append(f'<font color="green">{text}</font>')
            self.runLogsClearButton.setDisabled(False)

        self.worker.outputSignal.connect(output)

        def finished():
            self.runButton.setDisabled(False)
            App.alert(self, 0)
            if (
                App.applicationState()
                == Qt.ApplicationState.ApplicationInactive
            ):
                SystemTray().send(
                    "Emails sent!", "Go back to the app to see the logs."
                )
            self.finishSound.play()

        self.worker.finished.connect(finished)
        self.worker.start()


#
