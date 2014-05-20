#!/usr/bin/env python

from simh import SIMH
from pdpobj import ObjFile
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--simh",type=str,default=None,
                        help="Path to write SIMH script to")
    parser.add_argument("-e","--emulator",type=str,default=None,
                        help="Path to write console emulator script to")
    parser.add_argument("objects",type=str,nargs="*")
    args = parser.parse_args()

    emus = []
    if args.simh:
        emus.append(SIMH(open(args.simh,'w')))
    if args.emulator:
        emus.append(Emulator(open(args.emulator,'w')))

    for path in args.objects:
        o = ObjFile(path)
        for block in o.blocks:
            if block.typeval == 3: # TXT block
                for e in emus: e.load_address(block.location)
                for w in block.words:
                    for e in emus: e.deposit_word(w)

