#! /usr/bin/python
import AlimE3631A
alim=AlimE3631A.AlimE3631A("/dev/ttyUSB1")
res=alim.send("*IDN?");
#res=alim.send(str.encode("*IDN?"));
print( "Response : ["+res+"]")

print(alim.pwr())
#print(alim.pwr(1))

import  OscilloWavePro
osc = OscilloWavePro.OscilloWavePro('192.168.0.48')
print("osc connected")
osc.pp_digital()
osc.getDigitalBus(1,105)


osc.getDigitalWaveForms()

osc.getDigitalBus(1,1000)

setup=1 ; line= 1
cmd_line = ":".join(["VBS? 't=\"\"",
    "num_samples = app.LogicAnalyzer.Digital%d.Out.Result.Samples" % setup,
     "sample=0",   
     "last_sample=255",
     "res = app.LogicAnalyzer.Digital%d.Out.Result.DataArray(-1,1,0,%d)" % (setup, line),
     "for j = 0 To 250",
     "sample = res(j,0)",
     "If ( (last_sample) <> (sample) ) Then " "last_sample=sample:t = t & sample & \"@\" & j & \",\" " "End If",
     "Next",
     "return=t"
    ])    
print(cmd_line)
#samples = oszi.instr.ask(cmd_line)

def print_cmd(    setup=1, line= 1):
    cmd_line = ":".join(["VBS? '",
    "lines = app.LogicAnalyzer.Digital{}.Out.Result.Lines".format(setup),
    "val=0",   
    "res = app.LogicAnalyzer.Digital{}.Out.Result.DataArray(1,-1,{},0)".format(setup, sample),
    "for line = 0 To lines-1",
    "val=val + res(0,line)*2^line",
    "Next",
    "return=val'"
    ])    


def getDigitalWaveForm(self, setup=1, line= 1):
    cmd_line = ":".join(["VBS? 't=\"\"",
        "num_samples = app.LogicAnalyzer.Digital{}.Out.Result.Samples".format(setup),
         "sample=0",   
         "last_sample=255",
         "res = app.LogicAnalyzer.Digital{}.Out.Result.DataArray(-1,1,0,{})".format(setup, line),
         "for j = 0 To num_samples-1",
         "sample = res(j,0)",
         "If ( (last_sample) <> (sample) ) Then " "last_sample=sample:t = t & sample & \"@\" & j & \",\" " "End If",
         "Next",
         "return=t"
        ])    
    return self.send(cmd_line)


self=osc
[self.getDigitalWaveForm(i,n) for i in range(1,n+1) for n in self.pp_digital(False)]

print(list(enumerate( self.pp_digital(False),1)))
[(1, 13), (2, 3)]

osc.getDigitalBus(1,56)
[osc.getDigitalBus(1,55+12.5*i) for i in range(4)]
[osc.getDigitalBus(1,55+12.5*i) for i in range(13)]
osc.send("TDIV 1E-8")
osc.send('TDIV 500E-9')
osc.send('TDIV 100E-9')
osc.send("TDIV?")
VALID=osc.getDigitalWaveForm(2,0)
vals=VALID.split(",")
start=vals[1].split("@")[1]
stop=vals[2].split("@")[1]

TRFL DISK,HDD,FILE, 'file path'


osc.send("TDIV?")
telnet 192.168.0.48

# \USB Disk\PICMIC_PICS\pic30.jpg
# TRFL? DISK,<device>,FILE,’name.ext’
# CMD$=TRFL,DISK,FLPY,FILE,’FAVORITE.DSO’
# CALL IBWRT(DDA%,CMD$)

import  OscilloWavePro
osc = OscilloWavePro.OscilloWavePro('192.168.0.48')
osc.send("*IDN?")
osc.send("TRFL? DISK,HDD,\USB Disk\PICMIC_PICS\pic30.jpg,pic30.jpg") #=> FAILED
osc.send("TRFL? DISK,HDD,\\USB Disk\\PICMIC_PICS\\pic30.jpg,pic30.jpg") #=> Freez
osc.send("TRFL? DISK,HDD,FILE,\USB Disk\PICMIC_PICS\pic30.jpg")
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 20-21: truncated \UXXXXXXXX escape'

osc.send("TRFL? DISK,HDD,FILE,\'\USB Disk\PICMIC_PICS\pic30.jpg\'")
osc.send("TRFL? DISK,HDD,FILE,'\USB Disk\PICMIC_PICS\pic30.jpg'")
   osc.send("TRFL? DISK,HDD,FILE,'\USB Disk\PICMIC_PICS\pic30.jpg'")
                                                                    ^
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 21-22: truncated \UXXXXXXXX escape'
osc.send("TRFL? DISK,HDD,FILE,'\\USB Disk\\PICMIC_PICS\\pic30.jpg'")

  File "/home/pi/testbench/drivers/OscilloWavePro.py", line 70, in send
    end=tmp[-1:] if sys.version_info.major<3 else tmp[-1:].decode()
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 0: invalid start byte

# Probablement un PB avec la lecture des images pas ASCII
#=> abandon de cette methode. pour l instant '


import  OscilloWavePro
osc = OscilloWavePro.OscilloWavePro('192.168.0.48')
samples=osc.pp_digital(False)[2]
dt=osc.getVal("TDIV?")
xscale=dt*10
dx=xscale/(samples-2) # remove one and interval minus poteau
clk=25E-9
VALID=osc.getDigitalWaveForm(2,0)
vals=VALID.split(",")
vals.remove('')
if len(vals)<3:
    print("no falling edge => increase TDIV")
    osc.send('TDIV {}'.format(dt*2))
    # loop over previous [TODO] (reevaluate samples, dt, etc.

start=vals[1].split("@")[1]
stop=vals[2].split("@")[1]

nbVALID=int((int(stop)*dx-int(start)*dx)/clk)


[osc.getDigitalBus(1,55+12.5*i) for i in range(13)]
[osc.getDigitalBus(1,55+12.5*i) for i in range(nbVALID)]
MARKER=osc.getDigitalWaveForm(2,3).split(',')
trig=int(MARKER[2].split('@')[1]) #=>51
istep=clk/dx #=> 12.5
noiseMarge=4
[osc.getDigitalBus(1,trig+noiseMarge+istep*i) for i in range(nbVALID)]

import numpy as np
import os
data = np.loadtxt(os.path.expanduser("~/picmic/picmic0_SW_055/ROnb_xyp1.txt"))
# ^ marche pas car pas formater comme array

Filename=os.path.expanduser("~/picmic/picmic0_SW_055/ROnb_xyp1.txt")
with open (Filename,'r') as f:
    lines = f.readlines

file1 = open(Filename, 'r')
Lines = file1.readlines()

Line=Lines[0]
Line.replace('(', '')
#                                                       >>> [osc.getDigitalBus(
# hit nb:1, col :2, row:18, result:274(d) / 112 (x)     274=0x112=0b0000000100010010 ROW_18 COL_2    
# hit nb:2, col :4, row:19, result:531(d) / 213 (x)     531=0x213=0b0000001000010011 ROW_19 COL_4   
# hit nb:3, col :9, row:25, result:1177(d) / 499 (x)    1177=0x499=0b0000010010011001 ROW_25 COL_9  
# hit nb:4, col :10, row:22, result:1302(d) / 516 (x)   1302=0x516=0b0000010100010110 ROW_22 COL_10 
# hit nb:5, col :11, row:22, result:1430(d) / 596 (x)   1430=0x596=0b0000010110010110 ROW_22 COL_11 
# hit nb:6, col :11, row:23, result:1431(d) / 597 (x)   1431=0x597=0b0000010110010111 ROW_23 COL_11 
# hit nb:7, col :11, row:24, result:1432(d) / 598 (x)   1432=0x598=0b0000010110011000 ROW_24 COL_11 
# hit nb:8, col :11, row:25, result:1433(d) / 599 (x)   1433=0x599=0b0000010110011001 ROW_25 COL_11 
# hit nb:9, col :12, row:22, result:1558(d) / 616 (x)   1558=0x616=0b0000011000010110 ROW_22 COL_12 
# hit nb:10, col :13, row:22, result:1686(d) / 696 (x)  1686=0x696=0b0000011010010110 ROW_22 COL_13 
# hit nb:11, col :18, row:28, result:2332(d) / 91c (x)  6428=0x191c=0b0001100100011100 ROW_28 COL_50
# hit nb:12, col :19, row:27, result:2459(d) / 99b (x)  6555=0x199b=0b0001100110011011 ROW_27 COL_51
# hit nb:13, col :19, row:30, result:2462(d) / 99e (x)  6558=0x199e=0b0001100110011110 ROW_30 COL_51
# hit nb:14, col :20, row:27, result:2587(d) / a1b (x)  6683=0x1a1b=0b0001101000011011 ROW_27 COL_52
# hit nb:15, col :20, row:30, result:2590(d) / a1e (x)  6686=0x1a1e=0b0001101000011110 ROW_30 COL_52
# hit nb:16, col :25, row:32, result:3232(d) / ca0 (x)  7328=0x1ca0=0b0001110010100000 ROW_32 COL_57
# hit nb:17, col :25, row:33, result:3233(d) / ca1 (x)  7329=0x1ca1=0b0001110010100001 ROW_33 COL_57
# hit nb:18, col :26, row:33, result:3361(d) / d21 (x)  7457=0x1d21=0b0001110100100001 ROW_33 COL_58
# hit nb:19, col :27, row:34, result:3490(d) / da2 (x)  7586=0x1da2=0b0001110110100010 ROW_34 COL_59
# hit nb:20, col :29, row:33, result:3745(d) / ea1 (x)  7841=0x1ea1=0b0001111010100001 ROW_33 COL_61
# hit nb:21, col :33, row:40, result:4264(d) / 10a8 (x) 6312=0x18a8=0b0001100010101000 ROW_40 COL_49
# hit nb:22, col :35, row:39, result:4519(d) / 11a7 (x) 6567=0x19a7=0b0001100110100111 ROW_39 COL_51
# hit nb:23, col :43, row:45, result:5549(d) / 15ad (x) 7597=0x1dad=0b0001110110101101 ROW_45 COL_59
# hit nb:24, col :44, row:42, result:5674(d) / 162a (x) 7722=0x1e2a=0b0001111000101010 ROW_42 COL_60
# hit nb:25, col :44, row:45, result:5677(d) / 162d (x) 7725=0x1e2d=0b0001111000101101 ROW_45 COL_60
# hit nb:26, col :45, row:42, result:5802(d) / 16aa (x) 7850=0x1eaa=0b0001111010101010 ROW_42 COL_61
# hit nb:27, col :45, row:45, result:5805(d) / 16ad (x) 7853=0x1ead=0b0001111010101101 ROW_45 COL_61



#exec(open("test_picmic.py").read())

from class_tb_picmic0 import getValids
#getValids(osc,alim)


