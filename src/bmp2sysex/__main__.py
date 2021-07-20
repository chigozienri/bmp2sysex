#!/usr/bin/env python 
from PIL import Image
import numpy as np
import sys
import argparse 
import warnings

def main(path, white1=False):
    im = Image.open(path)
    if im.mode != '1':
        warnings.warn('Only 1-bit images are supported. Will convert to 1-bit')
    im = im.convert('1')
    if im.size != (16, 16):
        im.close()
        raise RuntimeError('Only 16x16 images are supported')
    arr = np.asarray(im).astype(np.int32)
    # White is 0, black is 1 => invert compared to PIL default
    if not white1:
        arr = 1 - arr
    string = ''.join(arr.flatten().astype('str').tolist())
    return(string)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert bitmap to SysEx')
    parser.add_argument('path', type=str, help='path to bitmap image')
    parser.add_argument('-w', '--white1', help='Interpret 1 as white')
    args = parser.parse_args()
    print(main(args.path, white1=args.white1))
