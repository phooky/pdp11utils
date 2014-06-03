#!/usr/bin/env python

from pdpobj import ObjFile, LdaFile
from emulator import Emulator
import serial
import argparse
import simh
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--simh",action="store_true",default=False,
                        help="Use SIMH")
    parser.add_argument("-e","--emulator",type=str,default=None,
                        help="Console emulator port")
    parser.add_argument("objects",type=str,nargs="*")
    args = parser.parse_args()

    emus = []
    s = None
    if args.simh:
        s = simh.SIMH("~/opt/bin/pdp11","./default.ini")
        emus.append(s)
    if args.emulator:
        s = Emulator(serial.Serial(args.emulator,9600,timeout=0.02))
        emus.append(s)

    for path in args.objects:
        if path.endswith(".lda"):
            o = LdaFile(path)
            for block in o.blocks:
                for e in emus: e.load_address(block.location)
                for w in block.words:
                    for e in emus: e.deposit_word(w)
            e.start(o.blocks[0].location)
            e.wait_for('READY')
            e.send('0')
            for block in range(203):
                sys.stdout.write(e.read(014000 * 2))

