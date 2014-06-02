#!/usr/bin/env python

from pdpobj import ObjFile
from emulator import Emulator
import serial
import argparse

class SIMH:
    def __init__(self,pipe):
        self.f = pipe
        self.addr = 0
        
    def load_address(self,address):
        self.addr = address

    def deposit_word(self, w):
        self.f.write("d {0} {1}\n".format(oct(self.addr),oct(w)))
        self.addr = self.addr + 2


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--simh",type=str,default=None,
                        help="Path to write SIMH script to")
    parser.add_argument("-e","--emulator",type=str,default=None,
                        help="Console emulator port")
    parser.add_argument("objects",type=str,nargs="*")
    args = parser.parse_args()

    emus = []
    s = None
    if args.simh:
        emus.append(SIMH(open(args.simh,'w')))
    if args.emulator:
        s = Emulator(serial.Serial(args.emulator,9600,timeout=0.02))
        emus.append(s)

    for path in args.objects:
        o = ObjFile(path)
        for block in o.blocks:
            if block.typeval == 3: # TXT block
                for e in emus: e.load_address(block.location)
                for w in block.words:
                    for e in emus: e.deposit_word(w)
    if s:
        s.start(0)
