import time

from PySide6.QtCore import Qt, QThread
from qfluentwidgets import (
    PlainTextEdit,
)

from utils.logger import logger
from utils.notifications import Notifications
from app import App

class EmailerThread(QThread):

    def __init__(self, box: PlainTextEdit, data: str):
        super().__init__()
        self.box = box
        self.data = data

    def output(self, text: str):
        logger.info(text)
        self.box.appendPlainText(text)

    def run(self):
        self.output("Emailing...")
        time.sleep(1)
        self.output(self.data)
        time.sleep(1)
        self.output("Emails sent!")
        App.alert(self.box, 0)
        App.applicationState()
        if(App.applicationState() == Qt.ApplicationState.ApplicationInactive):
            Notifications().send("Process finished!", "All emails have been sent.")
