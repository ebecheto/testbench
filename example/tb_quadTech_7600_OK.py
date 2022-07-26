#! /usr/bin/python

import AlimE3631A

alim=AlimE3631A.AlimE3631A("/dev/ttyUSB0")
self=alim
res=alim.send("CONF:FREQ 1000.00")
res=alim.send("CONF:FREQ 10000.00")
res=alim.send("CONF:PPAR CP")
res=alim.send("*IDN?")

# SOMME POLLING ISSUE. IF NO COMPLEX COMMANDE BEFORE QUESTION, NO ANSWER
res=alim.send("MEAS")#<= ONE COMMANDE BEFORE QUESTION
res=alim.send("FETCH?"); print res





# alim.send("MEAS")#<= ONE COMMANDE BEFORE QUESTION
# res=alim.send("*IDN?")
# #=> OK ANWSER
# alim.send("MEAS")#<= ONE COMMANDE BEFORE QUESTION
# res=alim.send("*STB?")
