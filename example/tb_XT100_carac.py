#!/usr/bin/python3
import time,sys; from numpy import arange; from time import sleep
import XT100, MSO
pul = XT100.XT100('169.254.222.53', 5025)
pul.send("*IDN?")# 'Colby Instruments,XT-100-050N,22031948,V1.14\r'
osc = MSO.MSO('169.254.222.26'); print( "Osc connected")

#fout=open("XT100/XT100_carac.dat", "w")


osc.send("*OPC;CLEAR;*OPC?") # equivalent clear sweep
#osc.send("*OPC;");osc.send("*WAI");
osc.send("ACQUIRE:STOPAFTER SEQUENCE;DESE 1;*ESE 1;*SRE 32;ACQUIRE:STATE ON")
osc.send("ACQUIRE:STATE ON")
osc.send("ACQUIRE:STATE?")
osc.send("*OPC")
osc.send("*OPC?")
pop=osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?"); #osc.send("*OPC?")
pop=int(pop);print(pop)



print("BEFORE WHILE")
while(pop<=200):
    opc=osc.send("*OPC?")
    print("popu:{} {}".format(pop,opc))
    pop=osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?")
    rien=osc.send("ACQUIRE:STATE ON;")
#    pop=osc.send("*WAI:MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?")
    opc=osc.send("*OPC?")
    print("popu:{}, opc: {}".format(pop, opc))
    pop=int(pop)


osc.send("ACQUIRE:STATE ON")
osc.send("ACQUIRE:STATE?")
osc.send("ACQuire?")
osc.send("ACQuire:STOPAfter?")
osc.send("ACQUIRE:MODE?")
osc.send("ACQuire:SEQuence:NUMSEQuence?")
osc.send("ACQuire:SEQuence:NUMSEQuence 200")


osc.send("MEASUREMENT:MEAS1:SOURCE?")
osc.send("ACQuire:NUMACq?")

# osc.send("ACQUIRE:STATE OFF;HORIZONTAL:RECORDLENGTH 1000;ACQUIRE:MODE SAMPLE;ACQUIRE:STOPAFTER SEQUENCE;DESE 1;*ESE 1;*SRE 32;ACQUIRE:STATE ON;*OPC;MEASUREMENT:MEAS1:RESUlts:CURRentacq:MEAN?")

osc.send("ACQUIRE:STATE OFF;HORIZONTAL:RECORDLENGTH 1000;ACQUIRE:MODE SAMPLE;")

osc.send("ACQUIRE:STOPAFTER SEQUENCE;DESE 1;*ESE 1;*SRE 32;ACQUIRE:STATE ON;")
osc.send("*OPC")
osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?")

osc.send("ACQUIRE:STATE?")
osc.send("ACQUIRE:MODE?")
osc.send("HORIZONTAL:RECORDLENGTH?")
#ACQuire:STOPAfter {RUNSTop|SEQuence}

#osc.send("DESE 1;*ESE 1;*SRE 0")
#osc.send("SOCKETServer:PROTOCol?")
osc.send("*OPC")
while(osc.send("*OPC?")==0):
    True


pul.send("MODE?")

pul.send("del 6000;*opc?")
pul.send("REL?") #=> '00...0110\r'
osc.send("CLEAR") # equivalent clear sweep
while(float(osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?"))<=200):
    print(float(osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?")))

osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?")

osc.send("CLEAR;*OPC?");
pop=int(osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?"));sleep(0.5)
while(pop<=200):
    pop=int(osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?"));sleep(0.5); osc.send("*OPC?")
    print("OO")

osc.send("CLEAR;*OPC?");int(osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?"));sleep(0.5);
# exec('int(osc.send(\"MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?\").strip(\"\\r> \")) \nsleep(0.5)')


pul.send("del 7000;*opc?")
pul.send("REL?") #=> '00...0110\r'
osc.send("CLEAR;*OPC?") # equivalent clear sweep
osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?");sleep(0.5); osc.send("*OPC?")
osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?");sleep(0.5)
osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?");sleep(0.5)
osc.send("MEASUREMENT:MEAS3:RESUlts:ALLAcqs:MEAN?");sleep(0.5)#<= second measure? get stuck if no sleep

pul.send("del 50000.00")#<== max intrument limit
pul.send("REL?") #=> '00...01111111\r'
pul.send("del 50001.00")
pul.send("DEL?") #=> '5.000000e-08\r'
# no warning when asking over limit delay, but does not change the delay


pul.send("del 00.00;")# take time (~ 2-sec) to release the delays


