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
