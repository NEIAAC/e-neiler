# General options:
# nuitka-project: --standalone
# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --include-data-files={MAIN_DIRECTORY}/resources
# Compilation mode, standalone everywhere, except on macOS there app bundle:
# nuitka-project-if: {OS} == "Darwin":
#    nuitka-project: --macos-create-app-bundle

import sys

from app import App
from window import Window

if __name__ == "__main__":
    app = App(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec())
