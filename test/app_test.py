import pytest

from PySide6.QtGui import QIcon, QPixmap

from app import App
from version import __version__
from utils import loader
from utils.constants import (
    AUTHOR_NAME,
    AUTHOR_DOMAIN,
    EXECUTABLE_NAME,
    LOGO_PATH,
)


@pytest.fixture(scope="session")
def qapp_cls():
    return App


def testAppMeta(qapp: App):
    assert qapp.applicationName() == "Test"
    qapp.setApplicationName(EXECUTABLE_NAME)
    assert qapp.applicationName() == EXECUTABLE_NAME
    assert qapp.applicationVersion() == __version__
    assert qapp.organizationName() == AUTHOR_NAME
    assert qapp.organizationDomain() == AUTHOR_DOMAIN
    assert (
        qapp.windowIcon().pixmap(16, 16).toImage()
        == QIcon(QPixmap(loader.resources(LOGO_PATH))).pixmap(16, 16).toImage()
    )
