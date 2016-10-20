#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import arange, concatenate
import time
date=time.strftime("%Y_%m_%d-%H_%M_%S"); jour, heure=date.split('-')
import OscilloWavePro, PulseGenerator81160A, AlimE3631A
osc = OscilloWavePro.OscilloWavePro('192.168.0.45'); print "Osc connected"
pul = PulseGenerator81160A.PulseGenerator81160A('192.168.0.47') ; print "pul connected"

# config scope parameters
configs=('PACU 5,BASE,C4','PACU 4,BASE,C3', 'F1:DEF EQN,\"AVG(C2+C1)\"')
configs=['PACU 1,AMPL,F1','PACU 2,MIN,F1','PACU 3,MAX,F1']+list(configs)

[osc.send(config) for config in configs]



#osc.send("F1:DEF?")
#osc.send("vbs 'app.SaveRecall.Waveform.SaveSource=\"F1\"'")
# A0=AlimE3631A.AlimE3631A("/dev/ttyUSB0")
# A1=AlimE3631A.AlimE3631A("/dev/ttyUSB1")
# A2=AlimE3631A.AlimE3631A("/dev/ttyUSB2")
# PT=AlimE3631A.AlimE3631A("/dev/ttyUSB3")
#alims=A0, A1, A2, PT #_____________________________check numbers v v v v #
alims=[AlimE3631A.AlimE3631A("/dev/ttyUSB{}".format(i)) for i in 0,1,2,3]
A0, A1, A2, PT = alims
#[ a.send("*IDN?") for a in alims]
#[ a.volt() for a in alims[:3]]
temp=PT.temps()
#temp='27'
pwr=" + ".join([i for s in A0.power(), A1.power(), A2.power(1) for i in s])
print ". Config :\n"+pwr+"\t"+temp


v18s=arange(1.7,2.1, 0.01)
#v18=v18s[0]
#A1.send("APPL P6V, {}, 1.0".format(v18))
i=1

ampls=arange(0.05, 0.4, 0.025)
ampls=concatenate((ampls, arange(0.4, 1.2+0.05, 0.2)))
#ampl=ampls[0]

fout=open("CMRR_"+date+"_{:02}.log".format(float(temp)), "w") ;fout.write("#" + pwr +"\n")
# TODO : loop on ampl, loop on V18 level

for ampl in ampls:
    pul.send("VOLT2 {}".format(ampl))# ; osc.send("CLSW")
    fout.write("\n")
    [osc.yfit(p) for p in (1, 2)]
    [osc.yfit(p) for p in (1, 2)]
    for v18 in v18s:
        A1.send("APPL P25V, {}, 1.0".format(v18))
        [osc.yfit(p) for p in (1, 2)]
        osc.send("CLSW")
        osc.send('F1:DEF EQN,\"AVG(C2-C1)\"')
        while float(osc.getMeasurement(4).SWEEPS)<=10:
            None
        vout=osc.getMeasurement(1).AVG
        osc.send('F1:DEF EQN,\"AVG(C2+C1)\"')
        while float(osc.getMeasurement(4).SWEEPS)<=10:
            None
        measures=osc.avgs()
        print "{}".format(v18)+"\t".join(["{:.02g}m".format(float(i)*1e3) for i in [vout]+measures])
        fout.write("{}\t{}".format(ampl,v18)+"\t"+"\t".join([vout]+measures)+'\n')


fout.close()
print "splot '"+fout.name+"' u 1:2:($4-$3) w lp"

