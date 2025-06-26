import os

from PySide6.QtCore import QStandardPaths

# Beware of changing these variable names as they are used in the deployment workflows to get required information
EXECUTABLE_NAME = "E-neiler"
AUTHOR_NAME = "NEIAAC"
AUTHOR_DOMAIN = "neiaac.com"

LOGO_PATH = os.path.join("images", "logo.png")

DATA_PATH = os.path.join(
    QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.GenericConfigLocation
    ),
    AUTHOR_NAME,
    EXECUTABLE_NAME,
)
"""Path to store app data on the system, usually this should not need to be changed."""
