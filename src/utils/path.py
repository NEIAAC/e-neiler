import os

def fromBase(suffix: str) -> str:
    current = os.path.dirname(os.path.realpath(__file__))
    root = os.path.abspath(os.path.join(current, "..", suffix))
    return root
