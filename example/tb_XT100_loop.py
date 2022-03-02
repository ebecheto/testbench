#!/usr/bin/python3
import time,sys; from numpy import arange; from time import sleep
import XT100, MSO
pul = XT100.XT100('169.254.222.53', 5025)
pul.send("*IDN?")# 'Colby Instruments,XT-100-050N,22031948,V1.14\r'
osc = MSO.MSO('169.254.222.26'); print( "Osc connected")
osc.send("ACQuire:SEQuence:NUMSEQuence 200")
osc.send("ACQUIRE:STOPAFTER SEQUENCE")

# osc.send("DESE 1;*ESE 1;*SRE 32") #<= pas besoin, si utilisation correcte de *OPC?


# #osc.send("CLEAR") # clear sweep pas besoin, Acquire ON RAZ
# osc.send("ACQUIRE:STATE ON; *OPC?")
# pop =osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?")
# mean=osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:MEAN?")
# sdev=osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:STDD?")
# pop=int(pop);print(pop, mean, sdev)


## INIT
fout=open("XT100/XT100_carac.dat", "w")
pul.send("STEP 0.5 ps")
pul.send("del 0;*opc?")
## LOOP
nb = int(50000 / 0.5)
for i in range(nb):
#    print(i), 
    rien=pul.send("INC;*OPC?")
    rien=osc.send("CLEAR;ACQUIRE:STATE ON; *OPC?")
    mean=osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:MEAN?")
    sdev=osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:STDD?")
    rel=int(pul.send("REL?")[8:],2) # relays
    dly=pul.send("DEL?") # delays
    datas=[str(i), mean, sdev, dly, rel]
    msg="\t".join(datas)
    print(msg)
    rien=fout.write(msg+'\n')
    if i%100 :
        fout.flush()
#    print(i)


# pul.send("del 0;*opc?")
# pul.send("del 7000;*opc?")
# pul.send("REL?") #=> '00...0110\r'
# pul.send("STEP?")
# pul.send("STEP 0.5")#=> bug nano
# pul.send("STEP 0.5 ps")
# pul.send("INC;*OPC?")
# pul.send("DEL?")
# pul.send("UNITS?")
# pul.send("UNITS ps")

# osc.send("CLEAR;*OPC?") # equivalent clear sweep

# pul.send("del 50000.00")#<== max intrument limit
# pul.send("REL?") #=> '00...01111111\r'
# pul.send("del 50001.00")
# pul.send("DEL?") #=> '5.000000e-08\r'
# # no warning when asking over limit delay, but does not change the delay

# pul.send("del 00.00;")# take time (~ 2-sec) to release the delays


