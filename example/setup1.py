#! /usr/bin/python

import AlimE3631A, OscilloWavePro, PulseGenerator81160A

pwr = AlimE3631A.AlimE3631A('/dev/ttyUSB0')
osc = OscilloWavePro.OscilloWavePro('192.168.0.45')
pul = PulseGenerator81160A.PulseGenerator81160A('192.168.0.53')

pul.send("VOLT 1.2")
pul.send("VOLT 1.2")

pwr.send("APPL P6V, 1.8, 1.0")
print pwr.send("MEAS:CURR:DC? P6V")
osc.send("CLSW")
print osc.getMeasurement(1)

