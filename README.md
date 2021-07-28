# bmp2sysex

This package is used to convert 1-bit 16x16 bitmap images (e.g. in bmp or png
format) to Roland Sound Canvas Dot Display SYSEX messages.

This has been tested on the following Roland Sound Canvas models:
* SC-55
* SC-55mkII
* SC-88

Installation
------------
```bash
git clone https://github.com/chigozienri/bmp2sysex
cd bmp2sysex
pip install .
```


Usage
-----
```
python -m bmp2sysex [-h] [-w WHITE1] path

Convert bitmap to SYSEX

positional arguments:
  path                  path to bitmap image

optional arguments:
  -h, --help            show this help message and exit
  -w WHITE1, --white1 WHITE1
                        If True, interpret 1 as white
```
