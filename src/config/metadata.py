import os

from PySide6.QtCore import QStandardPaths

APP_NAME = "E-neiler"
AUTHOR_NAME = "NEIAAC"
AUTHOR_DOMAIN = "neiaac.com"
LOGO_PATH = "icons/logo.png"

DATA_PATH = os.path.join(
    QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.GenericConfigLocation
    ),
    AUTHOR_NAME,
    APP_NAME,
)
"""Path to store app data on the system, usually this should not need be changed."""
