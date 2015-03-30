#!/usr/bin/env python

import socket,sys, time

class DelayGeneratorGFT1004:
    BUFFER_SIZE = 1024

    def __init__(self, ip='192.168.0.43', port=4000):
        self.name= "greenfields GFT1004"
        self.ip=ip
        self.port=port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.connect()
        # parfois on peut se connecter sans la bonne adresse ???
        self.send("IP {}".format(ip))
        
        self.response = ""
  
    def __del__(self):
        self.s.close()

    def connect(self):
        self.s.connect((self.ip, self.port))

    def send(self,MESSAGE):
        try:
            self.s.send(MESSAGE+'\n')
            if '?' in MESSAGE:
                self.response = self.s.recv(DelayGeneratorGFT1004.BUFFER_SIZE).strip()
        except socket.error as e:
            print e
            self.connect()
            self.send(MESSAGE+'\n')

    def setTrig(self, channel, trig):
        # todo: verif bon parametre
        fmt = "{},{}"
        if isinstance(channel, int):
            fmt = 'T'+fmt
        self.send(('TRIG '+fmt).format(channel, trig))

    def setDelay(self, channel, delay):
        fmt = "{},{}"
        if isinstance(channel, int):
            fmt = 'T'+fmt
        self.send(('DELAY '+fmt).format(channel, delay))
        
if __name__ == "__main__":
    import time
    g = DelayGeneratorGFT1004('192.168.0.43')
    g.send("*IDN?")
    print g.response
    while True:
        msg = raw_input()
        g.send(msg)
        print g.response
