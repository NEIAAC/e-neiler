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
        timestamped = f"[{datetime.now().strftime('%H:%M:%S')}] {text}"
        self.outputSignal.emit(timestamped)

    def run(self):
        try:
            self.output(
                f"{self.data}",
            )
        except Exception as e:
            self.output(str(e), "ERROR")
