#!/usr/bin/python2
import time; from numpy import arange, concatenate # from utiles import *
import  OscilloWavePro, PulseGenerator81160A, AlimE3631A
#from OscilloWavePro import closerVal

#t2=time.time()
print "linearity of larzic_2015",

A0,A1,A2=[AlimE3631A.AlimE3631A("/dev/ttyUSB{}".format(i)) for i in 0,1,2]
pwr=" + ".join([i for s in A0.power(), A2.power(), A1.power(1) for i in s])
print ". Config saved :\n"+pwr
osc = OscilloWavePro.OscilloWavePro('192.168.0.46'); print "osc connected. Wait for Pulser 8 second..."
pul = PulseGenerator81160A.PulseGenerator81160A('192.168.0.47') ; print "pul connected"

pacus="MAX, TA", "MIN, C2", "AMPL, C4" , "RISE, TA" , "FALL, C2"

[osc.send("PACU {}, {}".format(i+1,item)) for i, item in enumerate(pacus)]
ampls=arange(0.05, 0.4, 0.025)
ampls=concatenate((ampls, arange(0.4, 1.2+0.05, 0.2)))

[osc.send("C{}:VDIV {}".format(i, ampls[0]/6)) for i in 1,2]
# date=time.strftime("%Y_%m_%d-%H_%M_%S"); jour, heure=date.split('-')
print "\n# [] let's go for {}-step from {} to {}".format(
    len(ampls),ampls[0],ampls[-1])

for i in range(53,64):
    i+=1; t1=time.time()
    fout=open("EX_{:02}.log".format(i), "w") ;fout.write("#" + pwr +"\n")
    for ampl in ampls:
        t0=time.time(); print ampl, "\t",
        pul.send("VOLT2 {}".format(ampl))# ; osc.send("CLSW")
        osc.send("C4:VDIV {}".format(ampl/6))
#        ret=[osc.send("C{}:ASET FIND".format(p)) for p in (1,2)]
        [osc.yfit(p) for p in (1, 2)]
        while float(osc.getMeasurement(2).SWEEPS)<=10:
            True
        fout.write("{}\t{}".format(i,ampl)+"\t"+"\t".join(osc.avgs())+'\n')
        print "{:0.2f} sec.".format(time.time() - t0)
    osc.beep(3)
    raw_input("pause ch{}[DONE],{:0.2f} , next:{}".format(i,time.time()-t1,i+1)) if i<64 else True
    fout.close()

#print "[END] duration : {:0.2f} sec".format(time.time()-t2)

