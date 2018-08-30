#!/usr/bin/env python

from Converter.bspt.reader import bsp2json
import sys


if __name__ == '__main__':
    data = open(sys.argv[1], 'rb').read()
    print(bsp2json(data))
