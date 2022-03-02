#!/usr/bin/python2
import time,sys
from numpy import arange
# from utiles import *
import PulseGenerator81160A
print 'Wait 8sec, slow init'
pul = PulseGenerator81160A.PulseGenerator81160A('169.254.222.46')
print "pul connected"
#pul.senf("*IDN?")

pul.send("*TRG")


pul.send("PULSe:TDELay1?")
pul.send("PULSe:WIDTh1?")
pul.send(":PULS:DEL?")

            
# :PULSe:TRANsition[1|2]:TRAiling{<seconds
pul.send("PULSe:TRANsition2:TRAiling 1.2e-6")
pul.send("PULS:TRAN2:TRA 1.2e-6")



step=0.1
end=1.2
ampls=arange(0.05, end+step, step)

ret=pul.send("OUTP2:COMP 0FF")
print(ret+"? not egal a 0 ?")

sys.exit("Check IT")


j=0
for i,ampl in enumerate(ampls):
    print i, ampl
    pul.send("VOLT {}".format(ampl))
    print pul.send("VOLT?")


for i,ampl in enumerate(ampls):
    print i, ampl
    pul.send("VOLT {}".format(ampl))
#    print pul.send("VOLT?")

