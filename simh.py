
class SIMH:
    def __init__(self,pipe):
        self.f = pipe
        self.addr = 0
        
    def load_address(self,address):
        self.addr = address

    def deposit_word(self, w):
        self.f.write("d {0} {1}\n".format(oct(self.addr),oct(w)))
        self.addr = self.addr + 2
