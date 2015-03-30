#!/usr/bin/env python

import socket,sys

class PulseGenerator81160A:
    BUFFER_SIZE = 1024
    
    def __init__(self, ip, port=5025):
        self.name= "Agilent"
        self.ip=ip
        self.port=port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.connect()
        self.response = ""
        
    def __del__(self):
        self.s.close()
        
    def connect(self):
        self.s.connect((self.ip, self.port))

    def send(self,MESSAGE):
        try:
            self.s.send(MESSAGE+"\n")
            if '?' in MESSAGE:
                self.response = self.s.recv(self.BUFFER_SIZE)
        except socket.error as e:
            self.connect()
            self.send(MESSAGE)
            
    def setFrequency(self, freq):
        self.send("PULSe:FREQuency {}".format(freq))




if __name__ == '__main__':    
    pg = PulseGenerator81160A('192.168.0.53', 5025)
    print '''____exemple:____
             OUTPUT ON
             OUTPUT2 OFF
             VOLT 1.2
             FREQ 1KHz'''
    print 'To (q)uit, type q\nWait 8 seconds (slow to respond)\n'
    msg = "*IDN?"
    while msg != 'q':
        pg.send(msg)
        if '?' in msg:
            print pg.response
        msg = raw_input('>')

#A81.send("PULSe:POWer 1.2\n")
