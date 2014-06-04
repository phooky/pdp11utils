#!/usr/bin/env python

from pdpobj import ObjFile, LdaFile
from emulator import Emulator
import serial
import argparse
import simh
import struct
import sys
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--simh",action="store_true",default=False,
                        help="Use SIMH")
    parser.add_argument("-e","--emulator",type=str,default=None,
                        help="Console emulator port")
    parser.add_argument("images",type=str,nargs="*")
    args = parser.parse_args()

    emus = []
    s = None
    if args.simh:
        s = simh.SIMH("~/opt/bin/pdp11","./write.ini")
        emus.append(s)
    if args.emulator:
        s = Emulator(serial.Serial(args.emulator,9600,timeout=0.02))
        emus.append(s)

    lda = LdaFile('./pakwrt.lda')

    for block in lda.blocks:
        for e in emus: e.load_address(block.location)
        for w in block.words:
            for e in emus: e.deposit_word(w)

    startloc = lda.blocks[0].location
    cylsize = 014000 * 2
    for path in args.images:
        f = open(path)
        e.start(startloc)
        e.wait_for('READY')
        e.send('0')
        sys.stderr.write("Beginning image\n")
        for block in range(203):
            time.sleep(0.05)
            cyl = f.read(cylsize)
            e.wait_for('GO')
            time.sleep(0.05)
            sys.stderr.write("Got go\n")
            if len(cyl) < cylsize:
                cyl = cyl + '\x00'*(cylsize - len(cyl))
            cylenc = ''.join([struct.pack('BB',0x40+(ord(a)&0x0F),0x40+(ord(a)>>4)) for a in cyl])
            e.send( cylenc )
            sys.stderr.write("Cylinder {0} len {1} sent\n".format(block,oct(len(cyl))))
            sys.stderr.flush()

