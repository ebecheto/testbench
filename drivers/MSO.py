#!/usr/bin/env python

import socket,sys, errno

class MSO:
    BUFFER_SIZE = 32*1024
    MEAS=["MEAN", "MAX", "MIN", "STDD", "POPU"]
    def __init__(self, ip, port=4000):
        self.name= "Agilent"
        self.ip=ip
        self.port=port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()#<== now and then, connect need if using send. Otherwise, use senf into opened fifo from bypassPipe.py
        self.response = ""
        self.idn = self.send("*IDN?")
        self.stdin  = None
        self.stdout = None
        
    def __del__(self):
        self.s.close()
        
    def connect(self):
        self.s.connect((self.ip, self.port))

    def send(self,MESSAGE):
        try:
            self.s.send(MESSAGE+"\n")
            self.response='no ?'
            if '?' in MESSAGE:
                tmp=''
                while(tmp[-1:]!='\n'):
                    tmp+= self.s.recv(self.BUFFER_SIZE)
                self.response = tmp[:-1]
                # ret=""
                # self.response = self.s.recv(self.BUFFER_SIZE)
            return self.response.strip('\n')
        except socket.error as e:
            self.connect()
            self.send(MESSAGE)

    def getMeasurement(self, slot):
        return [self.send("MEASU:MEAS"+str(slot)+":SUBGROUP:RESUlts:ALLAcqs:"+m+"? \"OUTPUT1\"") for m in self.MEAS]

            
        
            


#  " PULS:TRAN2:TRA"

if __name__ == '__main__':    
    import readline
    readline.parse_and_bind("tab: complete")
    print 'Wait 8 seconds (slow to respond the 1st time)\n'
    osc = MSO('192.168.0.47', 5025)
    print '''____exemple:____
             OUTPUT ON
             OUTPUT?
             OUTPut2 OFF
             VOLT 1.2
             VOLT2?
             PULS:TRAN2 1.2e-6   #<= set leading edge to 1.2us
             PULS:TRAN2?         #<= gives the leading edge value
             PULS:TRAN2:TRA 1e-6 #<= set trailing edge to 1us
             OUTP2:COMP ON #<= Enable OUT2_ 'complementary'
             FREQ 1KHz'''
    print 'To (q)uit, type q\n'
    msg = "*IDN?"
    while msg != 'q':
        osc.send(msg)
        if '?' in msg:
            print osc.response
        msg = raw_input('>')

#A81.send("PULSe:POWer 1.2\n")
