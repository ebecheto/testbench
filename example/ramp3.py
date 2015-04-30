#!/usr/bin/python2
import time
from numpy import arange
# from utiles import *
import AlimE3631A, OscilloWavePro, PulseGenerator81160A

ajuste=True ; savePng=True # False
CH=1; PX=CH #<= CHANNEL and measure PARAM
NDIV=3      #<== negative division vertical offset the cursor
fname="LarzTOT_150pF"
log="ramp3_"

pw1 = AlimE3631A.AlimE3631A('/dev/ttyUSB0')#<== Agilent above
pw2 = AlimE3631A.AlimE3631A('/dev/ttyUSB1')#<== Agilent under
pw3 = AlimE3631A.AlimE3631A('/dev/ttyUSB2')#<== keithley => pt100 measure
osc = OscilloWavePro.OscilloWavePro('192.168.0.45')
Ag = PulseGenerator81160A.PulseGenerator81160A('192.168.0.53')

## # could be commented
## pw1.send("APPL P6V, 1.35, 1.0; APPL P25V, 3.3, 1.0 ") #<== setup power supply
## pw2.send("APPL P6V, 1.8, 1.0;  APPL P25V, 3.5, 1.0 ")

pt100=pw3.temperature()
osc.send("HCSU FILE, \"{}_{}C\"".format(fname, pt100))
osc.send("vbs 'app.SystemControl.CloseDialog'")#<== ferme le panel si ouvert
osc.send("PACU 3, AMPL, C3") #<== param en plus measure vin
tra=osc.send("C1:TRA?"),osc.send("C2:TRA?"),osc.send("C3:TRA?"),osc.send("C4:TRA?") #<== save teh empty 'caneva' for optimizePlus gif compression
osc.send("C1:TRA OFF;C2:TRA OFF;C3:TRA OFF;C4:TRA OFF;SCDP")
osc.send(";".join(tra))

ampls=arange(0.05, 10.0+0.1, 0.1)

date=time.strftime("%Y_%m_%d")
date_no_=time.strftime("%Y%m%d")
fout=open(log+"{}_{}C.log".format(date_no_,pt100), "w")
fout.write("# {} {}[Ohm] {}[deg C]\n".format(date, round(float(pw3.RES())), pt100))
idcs = pw1.current2() + pw2.current2()#<== tuple concat
vdcs= pw1.volt2() + pw2.volt2()
pw2.send("INST:SEL P6V")
idcs=["{:.2g}".format(float(i)) for i in idcs]#<== float rounding
vdcs=["{:.3g}".format(float(i)) for i in vdcs]#<== float rounding
fout.write("# VOLTS : {} \n# AMPS : {}\n".format(vdcs, idcs))
print "\n# [] let's go for {}-step from {} to {}".format(
    len(ampls),ampls[0],ampls[-1])
for ampl in ampls:
    print ampl, " ",
    Ag.send("VOLT {}".format(ampl))
    osc.send("CLSW")
    vdiv=osc.setMaxFit(NDIV=NDIV) if ajuste else None
    max=float(osc.getMeasurement(PX).AVG)
    vdiv=osc.send("C{}:VDIV {}".format(CH, max/(3+NDIV))) if ajuste else None
#    savePng and time.sleep(0.5) and   osc.printScreen()
    if savePng :
#        time.sleep(1)
        while float(osc.getMeasurement(PX).SWEEPS)< 10:
            pass
        osc.printScreen() 
    meas=osc.getMeasurement(PX)
    vin=float(osc.getMeasurement(3).AVG)
    maxi=float(meas.AVG)
    sdev=float(meas.SIGMA)
    fout.write("{}; {}; {}; {}; {}\n".format(ampl,maxi,sdev,vdiv,vin))
fout.write("# temp {};[AMP] {}; {}\n".format(pw3.temperature(), pw1.current2(), pw2.current2()))
fout.close()

