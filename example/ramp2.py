#!/usr/bin/python2
print "let's check [25  to -70 degree] the linearity of larzic_2014"
import time
from numpy import arange
# from utiles import *
import AlimE3631A, OscilloWavePro, PulseGenerator81160A

ajuste=True ; savePng=True
CH=1; PX=CH #<= CHANNEL and measure PARAM
NDIV=2
fname="linearzic_MAX_1"

## pwr = AlimE3631A.AlimE3631A('/dev/ttyUSB0')
## pw2 = AlimE3631A.AlimE3631A('/dev/ttyUSB1')
osc = OscilloWavePro.OscilloWavePro('192.168.0.45')
Ag = PulseGenerator81160A.PulseGenerator81160A('192.168.0.53')


osc.send("HCSU FILE, \"{}\"".format(fname))
ampls=arange(0.05, 0.9+0.01, 0.01)

temp=27
fout=open("ramp_{}.log".format(temp), "w")
fout.write("# {}\n".format(time.strftime("%Y_%m_%d")))
## fout.write("# CONSO :[A] {}; {}".format(pwr.current2(), pw2.current2()))
print "\n# [] let's go for {}-step from {} to {}".format(
    len(ampls),ampls[0],ampls[-1])
for ampl in ampls:
    print ampl, " ",
    Ag.send("VOLT {}".format(ampl))
    osc.send("CLSW")
    vdiv=osc.setMaxFit() if ajuste else None
    max=float(osc.getMeasurement(PX).AVG)
    vdiv=osc.send("C{}:VDIV {}".format(CH, max/(2+NDIV)))
#    savePng and time.sleep(0.5) and   osc.printScreen()
    if savePng :
#        time.sleep(1)
        while float(osc.getMeasurement(PX).SWEEPS)< 100:
            pass
        osc.printScreen() 
    meas=osc.getMeasurement(PX)
    maxi=float(meas.AVG)
    sdev=float(meas.SIGMA)
    fout.write("{}; {}; {}; {}\n".format(ampl,maxi,sdev,vdiv))
fout.close()

