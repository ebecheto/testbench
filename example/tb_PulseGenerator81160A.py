#!/usr/bin/python2
import time
from numpy import arange
# from utiles import *
import PulseGenerator81160A
print 'Wait 8sec, slow init'
pul = PulseGenerator81160A.PulseGenerator81160A('192.168.0.46')
print "pul connected"

step=0.1
end=1.2
ampls=arange(0.05, end+step, step)

j=0
for i,ampl in enumerate(ampls):
    print i, ampl
    pul.send("VOLT {}".format(ampl))
    print pul.send("VOLT?")


for i,ampl in enumerate(ampls):
    print i, ampl
    pul.send("VOLT {}".format(ampl))
#    print pul.send("VOLT?")

