#!/usr/bin/python2
print "let's check the linearity of larzic_2015"
print "larzic_2015 as a differential output buffer"
import time
from numpy import arange
# from utiles import *
import  OscilloWavePro, PulseGenerator81160A

ajuste=True ; savePng=False
CH=1; PX=CH #<= CHANNEL and measure PARAM
NDIV=2
fname="diff_CH"

osc = OscilloWavePro.OscilloWavePro('192.168.0.45')
print "osc connected"
pul = PulseGenerator81160A.PulseGenerator81160A('192.168.0.47')
print "pul connected"

# TODO externally : IRL (In Real Life)
#  put Channel 1 and 4 as positive ends of the diffenrential pairs

# not needed anymore, a use Trigger out from pulseGen => positiv
# osc.send("EX:TRSL NEG")
# osc.send("TRSE EDGE,SR,EX,HT,OFF")
osc.send("F1:DEF EQN,'C1-C2'")
osc.send("F2:DEF EQN,'C4-C3'")
osc.send("TRMD AUTO")  #<== Auto trigger mode needed for noise measurement

osc.send("HCSU FILE, \"{}\"".format(fname))
# osc.send("PACU 5, XMAX, F1")
ampls=arange(0.05, 1.2+0.1, 0.1)


NBSWEEP=10
temp=time.strftime("%Y_%m_%d-%H_%M_%S") # 27
foutName="ramp_{}.log".format(temp)
fout=open(foutName, "w")
print( "** writing to "+foutName + " **")
fout.write("# {}\n".format(temp))
## fout.write("# CONSO :[A] {}; {}".format(pwr.current2(), pw2.current2()))
## measure SDEV
pul.send("OUTPUT2 OFF")
[osc.setMeasureSlot(i+1,"SDEV,"+p) for i,p in enumerate(['F1','C1','C2','F2','C3','C4'])] # set P1-7
osc.send("TDIV 1E-3")
osc.send("CLSW")
#[osc.send("C{}:VDIV 1e-3".format(p)) for p in (1, 2, 3, 4)] # zoom calibre for sdev
[osc.setCaliber(ch, 1e-3) for ch in range(1,5)]
osc.send("CLSW")
while float(osc.getMeasurement(1).SWEEPS)< 10:
    pass
sdevs=[ osc.getMeasurement(p).AVG for p in (1,2,3,4,5,6)]
msg="#SDEV#"+";".join(sdevs)+'\n'
print "GOT:"+msg
pul.send("OUTPUT2 ON")
osc.send("TDIV 2E-6")
#[osc.send("C{}:VDIV 50e-3".format(p)) for p in (1, 2, 3, 4)] # unzoom calibre for mini pulse

fout.write("#__SDEV__\n"+msg)
print "\n# [] let's go for {}-step from {} to {}".format(
    len(ampls),ampls[0],ampls[-1])

[osc.setMeasureSlot(i+1,"MAX,"+p) for i,p in enumerate(['C1','C4','F1','F2'])] # set P1-4
[osc.setMeasureSlot(i+5,"MIN,"+p) for i,p in enumerate(['C2','C3'])]           # set P5-6

fout.write("#HEADER F1\tC1\tC2\tF2\tC4\tC3\t\n")

for ampl in ampls:
    print ampl, " "
    pul.send("VOLT2 {}".format(ampl))
    osc.send("CLSW")
    #[osc.setMaxFit(p, 1, NDIV=0, MAX='AMPL') for p in (1, 2, 3, 4)]
    [osc.optimizeCaliber(ch, ampl==ampls[0]) for ch in range(1,5)]
    measures=[osc.getMeasurement(p).AVG for p in (3,1,5,4,2,6)]
    msg="{}".format(ampl)+"\t"+"\t".join(measures)+'\n'
    fout.write(msg)
fout.close()
# screen dump for verif
osc.send("SCDP")
