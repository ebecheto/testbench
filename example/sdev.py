#!/usr/bin/python2
import  OscilloWavePro

osc = OscilloWavePro.OscilloWavePro('192.168.0.45')
print "osc connected"
osc.send("F1:DEF EQN,'C1-C2'")
osc.send("F2:DEF EQN,'C4-C3'")
osc.send("TRMD AUTO")  #<== Auto trigger mode needed for noise measurement

[osc.setMeasureSlot(i+1,"SDEV,"+p) for i,p in enumerate(['F1','C1','C2','F2','C3','C4'])] # set P1-7
[osc.setCaliber(ch, 1e-3) for ch in range(1,5)]
