#!/usr/bin/env python
import argparse
import warnings

import numpy as np
from PIL import Image


def main(path, white1=False):
    im = Image.open(path)
    if im.mode != "1":
        warnings.warn("Only 1-bit images are supported. Will convert to 1-bit")
    im = im.convert("1")
    if im.size != (16, 16):
        im.close()
        raise RuntimeError("Only 16x16 images are supported")
    arr = np.asarray(im).astype(np.int32)
    # White is 0, black is 1 => invert compared to PIL default
    if not white1:
        arr = 1 - arr

    # SYSEX Constant Bytes
    exclusiveStatus = 0xF0
    manufacturerID = 0x41
    deviceID = 0x10
    modelID = 0x45
    commandID = 0x12
    EOX = 0xF7

    address1 = 0x10
    address2 = 0x01
    address3 = 0x00

    # Init for use in checksum
    runningSum = address1 + address2 + address3

    # Init outputList
    outputList = [
        exclusiveStatus,
        manufacturerID,
        deviceID,
        modelID,
        commandID,
        address1,
        address2,
        address3,
    ]
    # Init Loop
    z = 0

    byte = 0

    # Loop through array and convert into SYSEX Bytes
    while z < 4:
        y = 0
        while y < 16:
            x = z * 5
            if z < 3:
                factor = 16
                byte = 0
                while x >= (z * 5) and x <= ((z * 5) + 4):
                    byte = byte + arr[y, x] * factor
                    factor = factor >> 1
                    x += 1
            else:
                byte = arr[y, x] * 16

            outputList.append(byte)
            runningSum = runningSum + byte

            byte = 0
            y += 1
        z += 1

    # Generate checksum
    checksum = 128 - (runningSum % 128)

    # Append checksum & EOX
    outputList.append(checksum)
    outputList.append(EOX)

    # Generate string
    bytes = [format(b, '02X') for b in outputList]
    return " ".join(bytes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert bitmap to Roland Sound Canvas Dot Display SYSEX message"
    )
    parser.add_argument("path", type=str, help="path to bitmap image")
    parser.add_argument(
        "-w", "--white1", help="Interpret 1 as white", action="store_true"
    )
    args = parser.parse_args()
    print(main(args.path, white1=args.white1))
