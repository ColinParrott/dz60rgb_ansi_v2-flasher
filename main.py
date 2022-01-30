import json
import os
import sys
from pathlib import Path
from typing import Dict

from usb.usb_handler import install_new_firmware
from utils import exit_program

CONFIG_PATH = sys.path[0] + os.sep + "flasher_config.json"


def read_config() -> Dict:
    if not Path(CONFIG_PATH).is_file():
        exit_program("Config file does not exist at %s" % CONFIG_PATH)

    with open(CONFIG_PATH, 'r') as f:
        return json.load(fp=f)


def validate_config(cfg: dict) -> bool:

    if "compiled_firmware_path" not in cfg:
        exit_program("'compiled_firmware_path' is missing in  the config file (%s)" % CONFIG_PATH)
    elif "target_firmware_name" not in cfg:
        exit_program("'target_firmware_name' is missing in  the config file (%s)" % CONFIG_PATH)
    elif "target_drive" not in cfg:
        exit_program("'target_drive' is missing in  the config file (%s)" % CONFIG_PATH)

    if not Path(cfg["compiled_firmware_path"]).is_file():
        exit_program("compiled_firmware_path does not exist")
        return False

    return True


if __name__ == '__main__':
    config = read_config()
    validate_config(config)
    install_new_firmware(config)
