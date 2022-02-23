#!/usr/bin/python2
import time,sys
from numpy import arange
# from utiles import *
import PulseGenerator81160A
print 'Wait 8sec, slow init'
pul = PulseGenerator81160A.PulseGenerator81160A('169.254.222.53', 5025)
print "pul connected"
# pul.senf("*IDN?")
pul.send("*IDN?")# 'Colby Instruments,XT-100-050N,22031948,V1.14\r'
# pul.send("del?")
# pul.send("net?")
# pul.send("step?")
# pul.send("ctstore? info")# 'DATE=2/1/2022_12:08:55_PM,SN=22031948,VNA=E5063A-MY54502577,MARKER_F=2777777777\r'
# pul.send("REL?") #=> '00000000000000000\r'

import MSO
osc = MSO.MSO('169.254.222.26'); print( "Osc connected")
#osc.send("MEASUREMENT:MEAS3:RESUlts:CURRentacq:MEAN?")
osc.send("CLEAR") # equivalent clear sweep
osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?")

pul.send("del 100")
pul.send("del 1000")
pul.send("REL?") #=> '00...0001\r'
pul.send("del 2000")
pul.send("REL?") #=> '00...0011\r'
pul.send("del 3000;*opc?")
pul.send("REL?") #=> '00...0100\r'
pul.send("del 4000;*opc?")
pul.send("REL?") #=> '00...0110\r'


pul.send("del 5000;*opc?")
pul.send("REL?") #=> '00...0110\r'
osc.send("CLEAR") # equivalent clear sweep
osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?")

pul.send("del 6000;*opc?")
pul.send("REL?") #=> '00...0110\r'
osc.send("CLEAR") # equivalent clear sweep
while(float(osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?").strip('\r> '))<=200):
    print(float(osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?").strip('\r> ')))

osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?")

osc.send("CLEAR;*OPC?"); pop=int(osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?").strip('\r> ')); print(pop)
while(pop<=200):
    pop=int(osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?").strip('\r> '))
    print("OO")


i=0
while(i<200):
    i+=1
    print("OO{}".format(i))



from time import sleep
pul.send("del 7000;*opc?")
pul.send("REL?") #=> '00...0110\r'
osc.send("CLEAR;*OPC?") # equivalent clear sweep
osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?");sleep(0.5); osc.send("*OPC?")
osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?");sleep(0.5)
osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?");sleep(0.5)
osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?");sleep(0.5)#<= second measure? get stuck if no sleep

