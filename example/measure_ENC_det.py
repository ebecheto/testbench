#!/usr/bin/python2
# -*- coding: utf-8 -*-
print "let's check the linearity of larzic_2015"
print "larzic_2015 as a differential output buffer"
import time
from numpy import arange
# from utiles import *
import  OscilloWavePro, PulseGenerator81160A

# polynomial fit function with a 4e10-3 accuracy convert pt100 resistor measured
def res2temp(r):
    return 6.76101314e-07*(r**3) + 7.62125457e-04*(r**2) + 2.38630456e+00*r - 2.46928114e+02

import argparse

parser = argparse.ArgumentParser(description='measure_ENC.py -pt100=113')
parser.add_argument('-pt100', type=float, default=113.0, help='temperature 27 deg <=> 113 Ohm of the PT100 probe')
parser.add_argument('-m', default='', help='comment to add in the file')
parser.add_argument('-cdet', default='', help='capa detector')
args = parser.parse_args()

cdet=args.cdet
pt100=args.pt100
comment=args.m
temperature=round(res2temp(pt100),2)


osc = OscilloWavePro.OscilloWavePro('192.168.0.45')            ;print "osc connected"
pul = PulseGenerator81160A.PulseGenerator81160A('192.168.0.47');print "pul connected"

# TODO externally : IRL (In Real Life)
# put Channel 1 and 4 as positive ends of the diffenrential pairs

# not needed anymore, a use Trigger out from pulseGen => positiv
# osc.send("EX:TRSL NEG")
# osc.send("TRSE EDGE,SR,EX,HT,OFF")
osc.send("F1:DEF EQN,'C1-C2'")
osc.send("F2:DEF EQN,'C4-C3'")
osc.send("TRMD AUTO")  #<== Auto trigger mode needed for noise measurement

# osc.send("PACU 5, XMAX, F1")
#step=0.1
#ampls=arange(0.03, 1.2+step, step)


NBSWEEP=10
time_str =time.strftime("%Y_%m_%d-%H_%M_%S") # 27
foutName="ENC_{}.log".format(time_str)
print( "** writing to "+foutName + " **")
print( "** temperature={} ".format(temperature) + " **")

## __ measure SDEV __ ##
pul.send("OUTPUT2 OFF")
[osc.setMeasureSlot(i+1,"SDEV,"+p) for i,p in enumerate(['F1','C1','C2'])] # set P1-3
# needed put scope in max memory to set TDIV abose 50us
osc.send('vbs app.Acquisition.Horizontal.Maximize="SetMaximumMemory"')
osc.send("TDIV 1E-3")
vdivs = [osc.getVal("C{}:VDIV?".format(ch+1)) for ch in range(2)]
offsets=[osc.getVal("C{}:OFST?".format(ch+1)) for ch in range(2)]

[osc.setCaliber(ch+1, 1e-3) for ch in range(2)]
while float(osc.getMeasurement(1).SWEEPS)< NBSWEEP:
    pass
sdevs=[float(osc.getMeasurement(p).AVG) for p in (1,2,3)]

# restare vdivs
osc.send("TDIV 2E-6")
[osc.setCaliber(ch+1, vdivs[ch], offsets[ch]) for ch in range(2)]
pul.send("OUTPUT2 ON")
ampl=pul.send("VOLT2?")
ampl=float(ampl)

# [osc.optimizeCaliber(ch) for ch in range(1,5)]
while float(osc.getMeasurement(1).SWEEPS)< NBSWEEP:
    pass

osc.setMeasureSlot(1,"MAX,F1")
osc.setMeasureSlot(2,"MAX,C1")
osc.setMeasureSlot(3,"MIN,C2")
# osc.setMeasureSlot(4,"MAX,F2")
# osc.setMeasureSlot(5,"MAX,C4")
# osc.setMeasureSlot(6,"MIN,C3")


measures=[float(osc.getMeasurement(p).AVG) for p in range(1,4)]
encs=[(sdevs[p]/measures[p]/1.6)*ampl*1e7 for p in range(3)]
#ENC=sdev/VOUT/1.6 * 1e7

with open(foutName, "w") as fout:
    fout.write("#Vin={}\ttemp={}\t\t{}\t\t{}\n".format(ampl, temperature, comment, time_str))
    fout.write("#HEADR#\tF1\tC1\tC2\tF2\tC4\tC3\t\n")

    fout.write("#SDEV#")
    for sdev in sdevs:
        fout.write("\t{}".format(sdev))
    fout.write('\n')

    fout.write("#VOUT#")
    for measure in  measures:
        fout.write("\t{}".format(measure))
    fout.write('\n')

    fout.write("ENC_"+cdet+"\t{}".format(temperature)+"°C")
    for enc in encs:
        fout.write("\t{}".format(enc))
    fout.write('\n')

with open(foutName, "r") as fout:
    print(fout.read())

from subprocess import call
call(["cat "+foutName+ "|xclip -i"],shell=True)
