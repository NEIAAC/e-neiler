from contextlib import contextmanager
import sys, os

@contextmanager
def suppressor():
    """
    Suppresses console output in guard statements.\n
    Example:\n
        with suppressStdout():
            print("Hello, World!")
    """
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
