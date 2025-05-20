import os
import sys


def loadFile(fileName: str) -> str:
    try:
        file = os.path.join(__compiled__.containing_dir, fileName)  # type: ignore
    except NameError:
        file = os.path.join(os.path.dirname(sys.argv[0]), fileName)
    return file


def loadResource(resourceName: str) -> str:
    file = loadFile(os.path.join("resources", resourceName))
    return file
