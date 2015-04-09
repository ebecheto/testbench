#!/usr/bin/python2
print "let's check [25  to -70 degree] the linearity of larzic_2014"
import time
from numpy import arange
# from utiles import *
import AlimE3631A, OscilloWavePro, PulseGenerator81160A

ajuste=True ; savePng=True
zoom=False
CHANNEL="C1"; PACU=1
fname="linear_zic_1"

pwr = AlimE3631A.AlimE3631A('/dev/ttyUSB0')
pw2 = AlimE3631A.AlimE3631A('/dev/ttyUSB1')
ws = OscilloWavePro.OscilloWavePro('192.168.0.45')
Ag = PulseGenerator81160A.PulseGenerator81160A('192.168.0.53')


ws.send("HCSU FILE, \"{}\"".format(fname))
ampls=arange(0.05, 0.9+0.01, 0.01)

temp=27
fout=open("ramp_{}.log".format(temp), "w")
fout.write("# {}\n".format(time.strftime("%Y_%m_%d")))
fout.write("# CONSO :[A] {}; {}".format(pwr.current2(), pw2.current2()))
print "\n# [] let's go for {}-step from {} to {}".format(
    len(ampls),ampls[0],ampls[-1])
for ampl in ampls:
    print ampl, " ",
    Ag.send("VOLT {}".format(ampl))
    ws.send("CLSW")
    vdiv=ws.setMaxFit() if ajuste else None
    ws.setMaxZoom(NUM=10) if zoom   else None
#    savePng and time.sleep(0.5) and   ws.printScreen()
    if savePng :
#        time.sleep(1)
        while float(ws.getMeasurement(PACU).SWEEP)< 100:
            pass
        ws.printScreen() 
    meas=ws.getMeasurement(PACU)
    maxi=float(meas.AVG)
    sdev=float(meas.SIGMA)
    fout.write("{}; {}; {}; {}\n".format(ampl,maxi,sdev,vdiv))
fout.close()

