import json
from pathlib import Path
from typing import Dict

from usb.usb_handler import install_new_firmware
from utils import exit_program

CONFIG_PATH = "flasher_config.json"


def read_config() -> Dict:
    with open(CONFIG_PATH, 'r') as f:
        return json.load(fp=f)


def validate_config(cfg: dict) -> bool:
    if not Path(cfg["compiled_firmware_path"]).is_file():
        exit_program("compiled_firmware_path does not exist")
        return False

    return True


if __name__ == '__main__':
    config = read_config()
    validate_config(config)
    install_new_firmware(config)
