import pytest

from app import App
from utils.constants import AUTHOR_NAME, AUTHOR_DOMAIN, EXECUTABLE_NAME

@pytest.fixture(scope="session")
def qapp_cls():
    return App

def testAppMeta(qapp: App):
    assert qapp.applicationName() == "pytest-qt-qapp"
    qapp.setApplicationName(EXECUTABLE_NAME)
    assert qapp.applicationName() == EXECUTABLE_NAME
    assert qapp.organizationName() == AUTHOR_NAME
    assert qapp.organizationDomain() == AUTHOR_DOMAIN
