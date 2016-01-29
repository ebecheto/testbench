#! /usr/bin/python
import time
import ThermalEnclosureWTL64, AlimE3631A
wt = ThermalEnclosureWTL64.ThermalEnclosureWTL64('192.168.0.44')
from D10strip import *

# definition des usbtty
for i in range(0,10,1):
    try:
        toto=AlimE3631A.AlimE3631A("/dev/ttyUSB{}".format(i))
    except :
        pass
    ## except AttributeError:
    ##     print "/dev/ttyUSB{} do not exist that is normal".format(i)
    else :
        id=toto.send("*IDN?").split(',')[2]
        if id=="0945322" :
            leak1 =toto
        elif id=="0687061":
            leak63=toto
        elif id=="0843376":
            leakGR=toto
        elif id=="0936675":
            HV =toto 

# print wt.getTemp(), wt.tempNominal

## import high voltage
def rampUP():
    for i in range (0, -800, -50):
        HV.send("SOUR:VOLT:LEV {}".format(i))
        itot=HV.send("READ?").split(',')[1]
        while float(itot) > 1e-3:
            print "C chaud "+ itot+" <== itot"
            itot=HV.send("READ?").split(',')[1]
        print i, itot
#     time.sleep(0.01)


CNT="50"
AGVS="SENS:AVER:COUNT "+CNT
HV.send(AGVS)
leak1.send(AGVS)
AGVS="CURR:AVER:COUNT "+CNT
leak63.send(AGVS)
leakGR.send(AGVS)
AGVS="SENS:AVER ON"
HV.send(AGVS)
leak1.send(AGVS)
AGVS="CURR:AVER:STAT ON"
leak63.send(AGVS)
leakGR.send(AGVS)


def measureAlli():
    itot=HV.send("READ?").split(',')[1]
    istrip63=leak63.send("MEAS:CURR?")
    istrip1=leak1.send("MEAS:CURR?").split(',')[1]
    iGR=leakGR.send("MEAS:CURR?")
    return itot, istrip63, istrip1, iGR


date=time.strftime("%Y-%m-%d_%H-%M-%S")

## HV.send("SOUR:VOLT:LEV 0")
## closeAll()
## HV.send("SOUR:VOLT:LEV -750")


## temps=[ 20.,  10.,   0., -10., -20., -30., -40., -50., -60., -70.]
## temps=[ -10., -20., -30., -40., -50., -60., -70.]
##temps=[40, 35, 30, 25, 20, 15, 10, 5, 0, -5, -10, -15, -20, -25, -30, -35, -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40]

wt.start = False
wt.setState()

#temps=[25.3]

temps=[40, 30, 25, 20, 15, 10, 5, 0, -5, -10, -15, -20, -25, -30, -35, -40, -25, -15, -5, 0, 10, 20, 25, 35, 20]
temps_check=[1,2,3]
wt.start=True
borne=0.1
for num, temp in enumerate(temps):
    wt.setTemp(temp)
    print wt.getTemp(), wt.tempNominal
    while not((temp - borne) <= wt.getTemp() and wt.getTemp() <= (temp + borne) ):
#    while not((temp + borne) < wt.getTemp() and wt.getTemp() > (temp - borne) ):#<== c'etait ca l'erreur
        print "True {} <= {} <= {} ".format((temp - borne), wt.getTemp(), (temp + borne))
        time.sleep(1*20)
        True
    print "True wait 30 min... {} < {} > {} ".format((temp + borne), wt.getTemp(), (temp - borne))


    for j, temp_check in enumerate(temps_check):
         if i>8 and i<19:
             time.sleep(20*60)
         else:
             time.sleep(5*60)
         fout2=open("Check_D18strip_{}_{:02d}_{}_{:02d}.dat".format(date, num, wt.getTemp(), j), "w")
         print "writting in {}:".format(fout2.name)
         fout2.write("# "+time.strftime("%Y-%m-%d_%H-%M-%S")+"; temp={}".format(wt.getTemp())+"\n")
         fout2.write("# i(strip) \t itot \t\t istrip1 \t istrip63 \t iGR\n")
         for i in range(1, 65):
            HV.send("SOUR:VOLT:LEV 0")
            channelSelectY(i)
            HV.send("SOUR:VOLT:LEV -750")
            time.sleep(0.5)
            itot, istrip63, istrip1, iGR = measureAlli()
            print i, itot, istrip63, istrip1, iGR
            fout2.write("{}".format(i)+"\t"+itot+"\t"+istrip1+"\t"+istrip63+"\t"+iGR+"\n")
         print "wrote in {}:".format(fout2.name)
         fout2.close()
    
        
    #time.sleep(2)
    fout=open("D18strip_{}_{:02d}_{}.dat".format(date, num, wt.getTemp()), "w")
    print "writting in {}:".format(fout.name)
    fout.write("# "+time.strftime("%Y-%m-%d_%H-%M-%S")+"; temp={}".format(wt.getTemp())+"\n")
    fout.write("# i(strip) \t itot \t\t istrip1 \t istrip63 \t iGR\n")
    for i in range(1, 65):
        HV.send("SOUR:VOLT:LEV 0")
        channelSelectY(i)
        HV.send("SOUR:VOLT:LEV -750")
        time.sleep(5)
        itot, istrip63, istrip1, iGR = measureAlli()
        print i, itot, istrip63, istrip1, iGR
        fout.write("{}".format(i)+"\t"+itot+"\t"+istrip1+"\t"+istrip63+"\t"+iGR+"\n")
    print "wrote in {}:".format(fout.name)
    fout.close()
    

HV.send("SOUR:VOLT:LEV 0")
wt.start = False
wt.setState()

    
    
    

# closeAll()

print "(: FINI :) "+ time.strftime("%Y-%m-%d_%H-%M-%S")
