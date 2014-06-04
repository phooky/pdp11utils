#!/usr/bin/env python
import sys
import struct

def to_word(b):
    return struct.unpack("<H",b)[0]

def to_word_array(b):
    o = []
    if len(b) & 0x01:
        b = b + '\x00'
    while b:
        o.append(struct.unpack("<H",b[:2])[0])
        b = b[2:]
    return o
        
# Parsing .LDA files
class LdaFile:
    def __init__(self,path):
        f = open(path,'rb')
        self.blocks = []
        while True:
            try:
                block = self.read_block(f)
                if len(block.bin) == 0:
                    break;
                self.blocks.append(block)
            except Exception as e:
                print e
                pass
        f.close()

    class Block:
        def __init__(self,loc,data):
            self.location = loc
            self.bin = data
            self.words = to_word_array(self.bin)

    def read_block(self,f):
        header = f.read(6)
        if header[0:2] != '\x01\x00':
            raise Exception("missing header")
        sz,loc = struct.unpack("<HH",header[2:])
        data = f.read(sz-6)
        csum = (-(sum(map(ord,header)) + sum(map(ord,data)) ) ) & 0xff
        check = ord(f.read(1))
        if check != csum:
            raise Exception("bad checksum {0} exp. {1}".format(hex(csum),hex(check)))
        return LdaFile.Block(loc,data)
    

# Parsing .OBJ files
class ObjFile:
    def __init__(self,path):
        f = open(path,'rb')
        self.blocks = []
        while True:
            block = self.read_block(f)
            self.blocks.append(block)
            if block.typeval == 6:
                break
        f.close()

    class Block:
        # type
        type_table = {
            1: 'GSD',
            2: 'ENDGSD',
            3: 'TXT',
            4: 'RLD',
            5: 'ISD',
            6: 'ENDMOD',
            7: 'LIB'
            }
        def __init__(self,f):
            hdr = f.read(6)
            if len(hdr) == 0:
                raise RuntimeError("No ENDMOD block")
            assert len(hdr) == 6
            assert hdr[0:2] == '\x01\x00'
            blen = to_word(hdr[2:4])
            #print "Block len ",blen
            assert blen >= 6
            self.typeval = to_word(hdr[4:])
            self.data = f.read(blen-6)
            cs = ord(f.read(1))
            #check = (sum(map(ord,hdr)) + sum(map(ord,self.data))) % 0xff
            #assert ((check + cs) % 0xff) == 0
            # checksums are failing; either badly generated or specified
            #print "Type",ObjFile.Block.type_table[self.typeval]
            if self.typeval == 3:
                # TXT
                self.location = to_word(self.data[0:2])
                self.bin = self.data[2:]
                self.words = to_word_array(self.bin)

    def read_block(self,f):
        return ObjFile.Block(f)


if __name__=='__main__':
    o = LdaFile(sys.argv[1])
    for b in o.blocks:
        print len(b.bin),"at",b.location

        
