import pathlib

from utils import get_file_checksum
import unittest


class TestChecksums(unittest.TestCase):

    def test_checksum_of_firmware_file_is_correct(self):
        test_file = pathlib.Path("test_res/test_firmware.bin")
        expected_checksum = "aaa506bfdfc2703ee115126e9c5fb90bb4ae2ed39d4a356f59daa5a07c3aca49"
        actual_checksum, valid = get_file_checksum(test_file)
        self.assertTrue(valid)
        self.assertEqual(expected_checksum, actual_checksum)


if __name__ == '__main__':
    unittest.main()
