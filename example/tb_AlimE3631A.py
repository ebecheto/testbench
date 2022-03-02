#! /usr/bin/python

import AlimE3631A

alim=AlimE3631A.AlimE3631A("/dev/ttyUSB0")

res=alim.send("*IDN?")
print "Response : ["+res+"]"

alim.SHAPe{SQUare}

alim.send("Freq 1KHz")
alim.send("FUNCtion:SHAPe SQUare")
