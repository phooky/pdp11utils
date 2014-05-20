#!/usr/bin/env python

import sys
from simh import SIMH
from pdpobj import ObjFile

if __name__ == '__main__':
    f = open('simh.script','w')
    s = SIMH(f)
    o = ObjFile('pakdump.out')
    for block in o.blocks:
        if block.typeval == 3: # TXT block
            s.load_address(block.location)
            for w in block.words:
                s.deposit_word(w)
    f.close()
