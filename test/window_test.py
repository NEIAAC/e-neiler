from PySide6 import QtCore
from pytestqt.qtbot import QtBot

from window import Window

def testSetup(qtbot: QtBot):
    window = Window()
    qtbot.addWidget(window)
    window.setWindowTitle("W1")
    window.show()

    assert window.isVisible()
    assert window.windowTitle() == "W1"

def testExitButton(qtbot: QtBot):
    window = Window()
    qtbot.addWidget(window)
    window.show()

    assert window.isVisible()

    qtbot.mouseClick(window.titleBar.closeBtn, QtCore.Qt.MouseButton.LeftButton)

    assert not window.isVisible()
