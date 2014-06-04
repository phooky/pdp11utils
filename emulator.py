import sys

class Emulator:
    def __init__(self,pipe):
        self.f = pipe
        self.addr = 0
        
    def load_address(self,address):
        self.f.write("L {0}\r".format(oct(address)))
        sys.stderr.write(self.f.read(100))

    def deposit_word(self, w):
        self.f.write("D {0}\r".format(oct(w)))
        self.addr = self.addr + 2
        sys.stderr.write(self.f.read(100))

    def start(self, address):
        self.load_address(address)
        self.f.write("S\r")

    def wait_for(self,s):
        # wait for 'READY'
        r = ''
        self.f.setTimeout(20)
        sys.stderr.write("Waiting for ready...")
        while r[-len(s):] != s:
            r = r + self.f.read(1)
        sys.stderr.write("Ready.\n")

    def send(self,s):
        self.f.write(s)

    def read(self,sz):
        self.f.setTimeout(120)
        b = self.f.read(sz)
        return b
        

