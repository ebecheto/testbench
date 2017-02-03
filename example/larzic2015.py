#!/usr/bin/python2
import time; from numpy import arange # from utiles import *
import  OscilloWavePro, PulseGenerator81160A, AlimE3631A
print "linearity of larzic_2015"


A0=AlimE3631A.AlimE3631A("/dev/ttyUSB0")
A1=AlimE3631A.AlimE3631A("/dev/ttyUSB1")
A2=AlimE3631A.AlimE3631A("/dev/ttyUSB2")
A3=AlimE3631A.AlimE3631A("/dev/ttyUSB3")
temp=A2.temps()
pwr=" + ".join([i for s in A0.power(), A1.power(1), A3.power() for i in s])

osc = OscilloWavePro.OscilloWavePro('192.168.0.45'); print "osc connected. Wait for Pulser 8 second..."
pul = PulseGenerator81160A.PulseGenerator81160A('192.168.0.47') ; print "pul connected"

osc.send("PACU 3, MIN, C3")
osc.send("PACU 4, MAX, C1")
osc.send("PACU 5, MAX, F1")
#ampls=arange(0.05, 5+0.05, 0.05)
ampls=arange(0.05, 1.2+0.05, 0.05)#=> 24 points

date=time.strftime("%Y_%m_%d-%H_%M_%S"); jour=date.split('-')[0]
fout=open("ramp_{}.log".format(date), "w")
fout.write("#" + pwr + ", temp=" +temp+ ", day=" + jour + "\n")
## fout.write("# CONSO :[A] {}; {}".format(pwr.current2(), pw2.current2()))
print "\n# [] let's go for {}-step from {} to {}".format(
    len(ampls),ampls[0],ampls[-1])
for ampl in ampls:
    print ampl, " "
    pul.send("VOLT2 {}".format(ampl))
    osc.send("CLSW")
    [osc.yfit(p) for p in (1, 3, 4)]
#    osc.yfit(4)
    measures=[ osc.getMeasurement(p).AVG for p in (3,4,5)]
    msg="{}".format(ampl)+"\t"+"\t".join(measures)+'\n'
    fout.write(msg)
fout.close()

