#! /usr/bin/python

import AlimE3631A

alim=AlimE3631A.AlimE3631A("/dev/ttyUSB2")

alim.send("a")
