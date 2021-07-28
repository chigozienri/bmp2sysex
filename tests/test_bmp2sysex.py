import tempfile
import warnings
from unittest import TestCase

import numpy as np
from PIL import Image

from bmp2sysex.__main__ import main


class TestMain(TestCase):
    def test_16x16_1bit_png(self):
        binary_image = "1010100000000001101010000000000011101000000000011010100000000000101010000000000100000000000000000000000000000001110101010111000010010101010100011001110101110000100101010101000111010101010100000000000000000001000000000000000000000000000000011010101010101010"  # noqa: E501
        expected = "F0 41 10 45 12 10 01 00 15 15 1D 15 15 00 00 1A 12 13 12 1A 00 00 00 15 00 00 00 00 00 00 00 15 15 15 15 15 00 00 00 0A 00 00 00 00 00 00 00 18 08 18 08 08 00 00 00 15 10 00 10 00 10 00 10 00 10 00 10 00 10 00 10 00 2E F7"
        # Invert 1 and 0 from PIL default before saving (1 - int(i))
        arr = (
            np.array([1 - int(i) for i in binary_image])
            .reshape((16, 16))
            .astype(np.bool)
        )
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            im = Image.fromarray(arr)
            im.mode = "1"
            im.save(tmp.name)
            self.assertEqual(main(tmp.name), expected)

    def test_16x16_1bit_bmp(self):
        binary_image = "1010100000000001101010000000000011101000000000011010100000000000101010000000000100000000000000000000000000000001110101010111000010010101010100011001110101110000100101010101000111010101010100000000000000000001000000000000000000000000000000011010101010101010"  # noqa: E501
        expected = "F0 41 10 45 12 10 01 00 15 15 1D 15 15 00 00 1A 12 13 12 1A 00 00 00 15 00 00 00 00 00 00 00 15 15 15 15 15 00 00 00 0A 00 00 00 00 00 00 00 18 08 18 08 08 00 00 00 15 10 00 10 00 10 00 10 00 10 00 10 00 10 00 10 00 2E F7"
        # Invert 1 and 0 from PIL default before saving (1 - int(i))
        arr = (
            np.array([1 - int(i) for i in binary_image])
            .reshape((16, 16))
            .astype(np.bool)
        )
        with tempfile.NamedTemporaryFile(suffix=".bmp") as tmp:
            im = Image.fromarray(arr)
            im.mode = "1"
            im.save(tmp.name)
            self.assertEqual(main(tmp.name), expected)

    def test_16x16_8bit(self):
        binary_image = "1010100000000001101010000000000011101000000000011010100000000000101010000000000100000000000000000000000000000001110101010111000010010101010100011001110101110000100101010101000111010101010100000000000000000001000000000000000000000000000000011010101010101010"  # noqa: E501
        arr = (
            np.array([255 * (1 - int(i)) for i in binary_image])
            .reshape((16, 16))
            .astype(np.bool)
        )
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            im = Image.fromarray(arr)
            im.mode = "L"
            im.save(tmp.name)
            with warnings.catch_warnings(record=True) as warning_list:
                main(tmp.name)
            self.assertIn(
                "Only 1-bit images are supported. Will convert to 1-bit",
                [str(warning.message) for warning in warning_list],
            )

    def test_8x8_1bit_png(self):
        binary_image = (
            "1010100000000001101010000000000011101000000000011010100000000000"
        )
        arr = (
            np.array([1 - int(i) for i in binary_image])
            .reshape((8, 8))
            .astype(np.bool)
        )
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            im = Image.fromarray(arr)
            im.mode = "1"
            im.save(tmp.name)
            with self.assertRaises(RuntimeError) as err:
                main(tmp.name)
            self.assertIn(
                "Only 16x16 images are supported", str(err.exception)
            )

    def test_white1(self):
        binary_image = "1010100000000001101010000000000011101000000000011010100000000000101010000000000100000000000000000000000000000001110101010111000010010101010100011001110101110000100101010101000111010101010100000000000000000001000000000000000000000000000000011010101010101010"  # noqa: E501
        expected = "F0 41 10 45 12 10 01 00 15 15 1D 15 15 00 00 1A 12 13 12 1A 00 00 00 15 00 00 00 00 00 00 00 15 15 15 15 15 00 00 00 0A 00 00 00 00 00 00 00 18 08 18 08 08 00 00 00 15 10 00 10 00 10 00 10 00 10 00 10 00 10 00 10 00 2E F7"
        # Save using PIL default (don't invert 1 and 0)
        arr = (
            np.array([int(i) for i in binary_image])
            .reshape((16, 16))
            .astype(np.bool)
        )
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            im = Image.fromarray(arr)
            im.mode = "1"
            im.save(tmp.name)
            self.assertEqual(main(tmp.name, white1=True), expected)
