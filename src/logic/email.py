from datetime import datetime

from PySide6.QtCore import QThread, Signal

from utils.logger import logger


class EmailerThread(QThread):
    outputSignal = Signal(str)

    def __init__(self, data: str):
        super().__init__()
        self.data = data

    def output(self, text: str, level="INFO"):
        logger.log(level, text)
        timestamped = f"[{datetime.now().strftime('%H:%M:%S')}] {text}\n"
        self.outputSignal.emit(timestamped)

    def run(self):
        try:
            self.output(
                "This is the start message, we will now wait for 3 seconds to simulate some work"
            )
            self.msleep(3000)

            self.output(
                f'You entered "{self.data}" in the input. We will now wait 3 more seconds'
            )
            self.msleep(3000)

            self.output(
                "Example finished, a sound was played. If the app is minimized it will also flash in the taskbar and you will receive a system notification"
            )
        except Exception as e:
            self.output(str(e), "ERROR")
