#!/usr/bin/env python
import sys
import struct

if __name__ == '__main__':
    for path in sys.argv[1:]:
        inf = open(path,'r')
        s = inf.read()
        inf.close()
        words = s.split()
        outf = open(path+'.bin','wb')
        for word in words:
            if len(word) > 6:
                outf.write(struct.pack("<H",int(word[:6],8)))
                outf.write(struct.pack("<H",int(word[6:],8)))
            else:
                outf.write(struct.pack("<H",int(word,8)))
        outf.close()

        
        
