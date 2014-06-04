#!/usr/bin/env python

from pdpobj import ObjFile, LdaFile
from emulator import Emulator
import serial
import argparse
import simh
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s","--simh",action="store_true",default=False,
                        help="Use SIMH")
    group.add_argument("-e","--emulator",type=str,default=None,
                        help="Console emulator port")
    args = parser.parse_args()

    emu = None
    s = None
    if args.simh:
        emu = simh.SIMH("~/opt/bin/pdp11","./default.ini")
    if args.emulator:
        emu = Emulator(serial.Serial(args.emulator,9600,timeout=0.02))

    o = LdaFile('pakdmp.lda')
    for block in o.blocks:
        emu.load_address(block.location)
        for w in block.words:
            emu.deposit_word(w)
    emu.start(o.blocks[0].location)
    emu.wait_for('READY')
    emu.send('0')
    for block in range(203):
        sys.stdout.write(emu.read(014000 * 2))

