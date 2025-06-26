import os
import sys
import tempfile

from PySide6 import QtCore

from utils.logger import logger, qMessageHandler
from app import App
from window import Window

if __name__ == "__main__":
    with logger.catch():
        QtCore.qInstallMessageHandler(qMessageHandler)

        app = App(sys.argv)

        window = Window()
        window.show()

        if "NUITKA_ONEFILE_PARENT" in os.environ:
            splash_filename = os.path.join(
                tempfile.gettempdir(),
                "onefile_%d_splash_feedback.tmp"
                % int(os.environ["NUITKA_ONEFILE_PARENT"]),
            )

            if os.path.exists(splash_filename):
                os.unlink(splash_filename)

        sys.exit(app.exec())
