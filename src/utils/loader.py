import os


def base(suffix: str) -> str:
    current = os.path.dirname(os.path.realpath(__file__))
    root = os.path.abspath(os.path.join(current, "..", suffix))
    return root


def resources(suffix: str) -> str:
    parsed = base(os.path.join("resources", suffix))
    return parsed
