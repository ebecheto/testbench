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
