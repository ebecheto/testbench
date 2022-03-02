#!/usr/bin/env python

import socket,sys, errno

class PulseGenerator81160A:
    
    
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
            self.s.send(MESSAGE+"\n")
            if '?' in MESSAGE:
                self.response = self.s.recv(self.BUFFER_SIZE)
            return self.response.strip('\n')
        except socket.error as e:
            self.connect()
            self.send(MESSAGE)

            
    def senf(self,MESSAGE):
        """
        bypassPipe.py should be launch before in order to prevent 8sec connection of the pulser
        os.mkfifo done in this files
        writes goes to   /tmp/pipe_2pul_192.168.0.47 #<== if self.ip is this ip
        reads comes from /tmp/pipe_2cli_192.168.0.47 #<== if self.ip is this ip
        """
        self.stdout  = open("/tmp/pipe_2pul_"+self.ip, 'w')
        self.stdout.write(MESSAGE+"\n")
        self.stdout.flush()
        self.stdout.close()
        
        if '?' in MESSAGE:
            self.stdin  = open("/tmp/pipe_2cli_"+self.ip, 'r', 0)#<== now fifo in listen mode wait bypass to close it
            self.response = self.stdin.read()
        return self.response
        
            
    def setFrequency(self, freq):
        self.send("PULSe:FREQuency {}".format(freq))

    def setTrail(self, edge='1e-6'):
        """set Trailing edge to ie. 1us if edge="1e-6"
        """
        self.send("PULSe:TRANsition1:TRAiling {}".format(edge))


#  " PULS:TRAN2:TRA"

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
             OUTPUT ON
             OUTPUT?
             OUTPut2 OFF
             VOLT 1.2
             VOLT2?
             PULS:TRAN2 1.2e-6   #<= set leading edge to 1.2us
             PULS:TRAN2?         #<= gives the leading edge value
             PULS:TRAN2:TRA 1e-6 #<= set trailing edge to 1us
             OUTP2:COMP ON #<= Enable OUT2_ 'complementary'
             FREQ 1KHz''')
    print( 'To (q)uit, type q\n')
    msg = "*IDN?"
    while msg != 'q':
        pg.send(msg)
        if '?' in msg:
            print( pg.response)
        msg = raw_input('>')

#A81.send("PULSe:POWer 1.2\n")
