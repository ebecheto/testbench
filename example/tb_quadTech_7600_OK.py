#! /usr/bin/python

import AlimE3631A

alim=AlimE3631A.AlimE3631A("/dev/ttyUSB0")
self=alim
res=alim.send("CONF:FREQ 1000.00")
res=alim.send("CONF:FREQ 100000.00")
res=alim.send("CONF:PPAR CP")
#res=alim.send("*IDN?")

# SOMME POLLING ISSUE. IF NO COMPLEX COMMANDE BEFORE QUESTION, NO ANSWER
res=alim.send("MEAS")#<= ONE COMMANDE BEFORE QUESTION
res=alim.send("FETCH?"); print res

fout=open("cap_injection.dat", "w")

for i in range(100):
    alim.send("MEAS")#<= ONE COMMANDE BEFORE QUESTION
    res=alim.send("FETCH?")
    print res
    rien=fout.write(res+'\n')



fout.close()
