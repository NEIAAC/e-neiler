import os
import sys

from utils.logger import logger


def getFilePath(fileName: str) -> str:
    locations = (
        # Files bundled inside the single binary build
        os.path.join(os.path.dirname(__file__), os.pardir),
        os.path.dirname(__file__),
        # Files in the directory the single binary build is in
        os.path.dirname(sys.argv[0]),
    )
    try:
        # Files in the standalone build directory
        locations = locations + (__compiled__.containing_dir,)  # type: ignore
    except NameError:
        pass

    for location in locations:
        filePath = os.path.abspath(os.path.join(location, fileName))
        if os.path.isfile(filePath):
            logger.debug(f"Returning file path: {filePath}")
            return filePath
    logger.error(
        f"Got a request to load file {fileName} but it could not be found, returning empty string"
    )
    return ""


def getResourcePath(resourceName: str) -> str:
    resourcePath = getFilePath(os.path.join("resources", resourceName))
    return resourcePath
