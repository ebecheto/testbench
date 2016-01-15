#!/usr/bin/python2
import  OscilloWavePro

osc = OscilloWavePro.OscilloWavePro('192.168.0.45')
print "osc connected"

# C2:TRA? #==> C2:TRA ON  #==> 'ON' or 'OFF'

for ch in range(1,5):
    ONt=osc.send("C{}:TRA?".format(ch))
    if ONt.split(" ")[1]=='ON':
        print "adjust Y scale for C{}".format(ch)
        osc.optimizeCaliber(ch, None)
    else:
        print "skip disabled channel C{}".format(ch)


