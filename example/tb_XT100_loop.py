#!/usr/bin/python3
import time,sys; from numpy import arange; from time import sleep
import XT100, MSO
pul = XT100.XT100('169.254.222.53', 5025)
pul.send("*IDN?")# 'Colby Instruments,XT-100-050N,22031948,V1.14\r'
osc = MSO.MSO('169.254.222.26'); print( "Osc connected")
osc.send("ACQuire:SEQuence:NUMSEQuence 200")
osc.send("ACQUIRE:STOPAFTER SEQUENCE")

osc.send("DESE 1;*ESE 1;*SRE 32") #<= pas besoin, si utilisation correcte de *OPC?


# #osc.send("CLEAR") # clear sweep pas besoin, Acquire ON RAZ
# osc.send("ACQUIRE:STATE ON; *OPC?")
# pop =osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:POPUlation?")
# mean=osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:MEAN?")
# sdev=osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:STDD?")
# pop=int(pop);print(pop, mean, sdev)

#3.935000e-08
#pul.send("del 50 ns;*opc?")
#pul.send("del 39.35 ns;*opc?")
# pul.send("REL?") # 0000000000111110
# pul.send("del 39.40 ns;*opc?")
# pul.send("REL?") # 0000000001101111
# pul.send("CTSTORE?") #=> '1' calibration table in use
# pul.send("CTSTORE? info")
# 'DATE=2/1/2022_12:08:55_PM,SN=22031948,VNA=E5063A-MY54502577,MARKER_F=2777777777'
# 0.625*62 = 38.75
# 0.625*63 = 39.375


start=39350#0
step=2.5# ps
stop=42000#<= 50ns max depth
## INIT
fout=open("XT100_carac_"+str(start)+"_"+str(stop)+"_"+str(step)+".dat", "w")
fout.write("# "+"\t".join(["i", "mean_dly", "sdev_dly", "riseTime", "riseTime_input"])+'\n')
pul.send("STEP "+str(step)+" ps")
pul.send("del "+str(start)+";*opc?")
pul.send("del?")
## LOOP
i=0
nb = int((stop-start) / step)
i=1

for i in range(nb):
#    print(i), 
    rien=pul.send("INC;*OPC?")
    rien=osc.send("CLEAR;ACQUIRE:STATE ON; *OPC?")
    mean=osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:MEAN?")
    sdev=osc.send("MEASU:MEAS3:RESUlts:ALLAcqs:STDD?")
    rel=int(pul.send("REL?")[8:],2) # relays
    rt1050=osc.send("MEASU:MEAS4:RESUlts:ALLAcqs:MEAN?")
    rtin=osc.send("MEASU:MEAS6:RESUlts:ALLAcqs:MEAN?")# RiseTime
    dly=pul.send("DEL?") # delays
    datas=[str(i), mean, sdev, dly, str(rel), rt1050, rtin]
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


