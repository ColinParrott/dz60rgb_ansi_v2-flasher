# DZ60RGB-ANSI v2 Windows  Flasher
This is a python script for quickly flashing the [DZ60RGB-ANSI v2](https://kbdfans.com/products/dz60rgb-ansi-mechanical-keyboard-pcb) keyboard on Windows, in particular, the 
`dztech/dz60rgb_ansi/v2_1` model (as listed in QMK) which normally requires you to manually copy and paste the firmware onto the keyboard's storage.

The script does the following:
1. Backup the existing firmware (`FLASH.bin`) to a `firmware_backup/` folder beside the script
2. Copy over the new firmware
3. Verify the new firmware has been installed successfully (checksum check)
4. Safely eject the keyboard's USB bootloader from Windows
5. Restart the keyboard (works most of the time)

## Requirements

* Python >= 3.10

### Python dependencies
* pywin32 >= 303
* WMI >= 1.5.1

See `[tool.poetry.dependencies]` in `pyproject.toml` for the exact python dependencies if you're not using [Poetry](https://python-poetry.org/).

## Usage
1. Download the repo and place it somewhere
2. Configure `flasher_config.json` where:
   * `compiled_firmware_path` is the location of the new firmware file (file will automatically be renamed to value of `target_firmware_name`)
   * `target_firmware_name` do **not** change this, it has to be  `FLASH.bin` for this particular model
   * `target_drive` name of the  keyboard as it appears in bootloader mode (should not need changed either)
3. Run the script via (it will wait for the keyboard) :
> python main.py

4. Plug in the keyboard in bootloader mode (Hold ESC then plug in the keyboard)
5. Flashing will begin (or stop if any errors arise)
6. If the keyboard doesn't restart after flashing, then unplug and plug your keyboard back in