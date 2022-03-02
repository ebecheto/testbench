#!/usr/bin/env python

import socket,sys, errno

class XT100:
    
    
    def __init__(self, ip, port=5025, BUFFER_SIZE = 1024):
        self.BUFFER_SIZE = BUFFER_SIZE
        self.name= "Agilent"
        self.ip=ip
        self.port=port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()#<== now and then, connect need if using send. Otherwise, use senf into opened fifo from bypassPipe.py
        self.response = ""
#        self.idn = self.send("*IDN?")
        self.stdin  = None
        self.stdout = None
        
    def __del__(self):
        self.s.close()
        
    def connect(self):
        self.s.connect((self.ip, self.port))

    def send(self,MESSAGE):
        try:
            msg = MESSAGE+'\n' if sys.version_info.major<3 else str(MESSAGE+'\n').encode('utf-8')
            self.s.send(msg)
            if '?' in MESSAGE:
                tmp=self.s.recv(self.BUFFER_SIZE)
                self.response = tmp if sys.version_info.major<3 else tmp.decode()
            return self.response.strip('\n').strip('\r')
        except socket.error as e:
            self.connect()
            self.send(MESSAGE)

    def getRelay(self):
        """ got only 7 relays in the version, but 16-bit are output
        i prefer to see only the last 8-bit, even if the MSB will allways be zero
        """
        return self.send("REL?")[8:]

    def error(self):
        return self.send("*ERR?")

    def mode(self):
        return self.send("MODE?")


#USAGE for shell test (not import from python)
#python drivers/PulseGenerator81160A.py -ip '169.254.222.26'
if __name__ == '__main__':    
    import readline
    readline.parse_and_bind("tab: complete")
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', default='169.254.222.45')
    args = parser.parse_args()
    ip=args.ip

    print( 'Wait 8 seconds (slow to respond the 1st time)\n')
    pg = PulseGenerator81160A(ip, 5025)
    print( '''____exemple:____
             del 100
             del?
             REL?
             *opc?''')
    print( 'To (q)uit, type q\n')
    msg = "*IDN?"
    while msg != 'q':
        pg.send(msg)
        if '?' in msg:
            print( pg.response)
        msg = raw_input('>')

#A81.send("PULSe:POWer 1.2\n")
