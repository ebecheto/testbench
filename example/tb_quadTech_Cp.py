#! /usr/bin/python
import AlimE3631A,sys

capa='C26' if len(sys.argv) < 2 else sys.argv[1]
alim=AlimE3631A.AlimE3631A("/dev/ttyUSB0")
self=alim
res=alim.send("CONF:FREQ 1000.00")
res=alim.send("CONF:FREQ 100000.00")
res=alim.send("CONF:PPAR CP")
res=alim.send("CONF:SPAR RP")
#res=alim.send("*IDN?")

# SOMME POLLING ISSUE. IF NO COMPLEX COMMANDE BEFORE QUESTION, NO ANSWER
res=alim.send("MEAS")#<= ONE COMMANDE BEFORE QUESTION
res=alim.send("FETCH?"); print res

# freqs=[10**i for i in range(7)]
# freqs=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 2000000]
# freqs=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000,950000,1000000,1500000, 2000000]
freqs=[100,150,200,300,400,500,600,700,800,900,1000,1500,2000,3000,4000,5000,6000,7000,8000,9000,10000,15000,20000,30000,40000,50000,60000,70000,80000,90000,100000,150000,200000,300000,400000,500000,600000,700000,800000,900000,950000,1000000,1250000,1500000,1750000,2000000]
cd
N=len(freqs)

fout=open("cap_"+capa+"_injection.dat", "w")
for j in range(N):
    freq=freqs[j]
    for i in range(5):
        alim.send("CONF:FREQ "+str(freq))
        alim.send("MEAS")#<= ONE COMMANDE BEFORE QUESTION
        res=alim.send("FETCH?")
        msg=str(freq)+'\t'+res
        print msg
        rien=fout.write(msg+'\n')
    rien=fout.write('\n')



fout.close()
