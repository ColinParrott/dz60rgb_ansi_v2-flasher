import pathlib
import sys
import hashlib
from typing import Tuple


def exit_program(message: str, code: int = 1):
    print("ERROR: %s" % message)
    print("Exiting...")
    sys.exit(code)


def get_file_checksum(file_path: pathlib.Path) -> Tuple[str, bool]:
    if not file_path.is_file():
        return "", False

    m = hashlib.sha256()
    with open(str(file_path), 'rb') as f:
        for chunk in iter(lambda: f.read(1024), b""):
            m.update(chunk)
    return m.hexdigest(), True
