import os
import pathlib
import shutil
import subprocess
import sys
import time
from typing import Dict

import wmi

from utils import exit_program, get_file_checksum

BACKUP_FOLDER = pathlib.Path(os.getcwd() +  "/firmware_backup")


def install_new_firmware(config: Dict):
    print("Starting flashing process...")
    keyboard_drive = get_keyboard_usb_drive(config["target_drive"])
    time.sleep(1)
    new_fw_path = config["compiled_firmware_path"]
    new_firmware_checksum = get_file_checksum(pathlib.Path(new_fw_path))

    # check there's enough space for the new firmware and remove old firmware
    installed_firmware_path = get_current_firmware_path(keyboard_drive, config)
    check_enough_space(installed_firmware_path, keyboard_drive, config)
    remove_and_backup_old_firmware(installed_firmware_path)

    # install and verify new firmware
    copy_over_new_firmware(new_fw_path, installed_firmware_path)
    verify_new_firmware(new_firmware_checksum, installed_firmware_path)

    time.sleep(0.5)
    # safely eject keyboard
    eject_keyboard(keyboard_drive)

    print("Done. New firmware flashed successfully!")


def get_keyboard_usb_drive(drive_name: str) -> wmi._wmi_object:
    print("Waiting on keyboard to be connected in bootloader mode... (CTRL-C to cancel)")
    found = False
    while not found:
        try:
            time.sleep(0.5)
            potential_drives = [wmi_object for wmi_object in wmi.WMI().Win32_LogicalDisk() if
                                wmi_object.description == "Removable Disk" and wmi_object.volumename == drive_name and wmi_object.filesystem == "FAT"]

            num_drives = len(potential_drives)
            if num_drives == 1:
                drive = potential_drives[0]
                print("Found removable disk named %s at %s" % (drive_name, drive.deviceid))
                return drive
            elif num_drives > 1:
                exit_program("Found more than 1 drive named %s. There must only be 1 present" % drive_name)
        except KeyboardInterrupt as e:
            print("CTRL-C pressed. Exiting")
            sys.exit(0)


def get_current_firmware_path(drive, config) -> pathlib.Path:
    old_fw_path = pathlib.Path(drive.deviceid + os.sep).joinpath(config["target_firmware_name"])
    if old_fw_path.is_file():
        return old_fw_path
    else:
        exit_program("Failed to find currently installed firmware at: %s" % old_fw_path)


def check_enough_space(current_fw_path, drive, config):
    # get size of old and new firmwares in bytes
    old_fw_size = pathlib.Path(current_fw_path).stat().st_size
    new_fw_size = pathlib.Path(config["compiled_firmware_path"]).stat().st_size
    free_space_after_removing_old = int(drive.freespace) + old_fw_size

    if new_fw_size >= free_space_after_removing_old:
        exit_program("Not enough space on keyboard: new_firmware_size=%d, free_space=%d" % (
            new_fw_size, free_space_after_removing_old))


def remove_and_backup_old_firmware(path):
    if not BACKUP_FOLDER.is_dir():
        os.mkdir(BACKUP_FOLDER)

    print("Removing current firmware...")
    shutil.move(path, BACKUP_FOLDER.joinpath(path.name))


def copy_over_new_firmware(existing_path: pathlib.Path, new_path: pathlib.Path):
    print("Copying over new firmware...")
    shutil.copy2(str(existing_path), str(new_path))


def verify_new_firmware(actual_firmware_checksum, new_path: pathlib.Path):
    print("Verifying new firmware...")
    if not new_path.is_file():
        exit_program(
            "Failed to verify new firmware: no firmware exists on the device. Please flash manually with the old firmware found in: %s" % str(
                BACKUP_FOLDER))

    installed_firmware_checksum = get_file_checksum(new_path)
    if installed_firmware_checksum != actual_firmware_checksum:
        exit_program(
            "Failed to verify new firmware: the checksum did not match. Please flash manually with the old firmware found in: %s" % str(
                BACKUP_FOLDER))


def eject_keyboard(drive: wmi._wmi_object):
    proc = subprocess.run(
        args=[
            'powershell',
            '$vol = get-wmiobject -Class Win32_Volume | where{$_.label -eq \'%s\'}; $Eject =  New-Object -comObject Shell.Application; $Eject.NameSpace(17).ParseName($vol.driveletter).InvokeVerb(“Eject”);' % drive.volumename
        ],
        text=True,
        stdout=subprocess.PIPE
    )

    if proc.returncode == 0:
        print("Safely ejected keyboard")
    else:
        print("Failed to safely eject keyboard. Try manually doing it or just unplug the keyboard if you can't")