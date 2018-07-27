import MPTDC, AlimE3631A, OscilloWavePro, time
osc = OscilloWavePro.OscilloWavePro('169.254.222.45'); print "Osc connected"
tdc=MPTDC.MPTDC(0x77)
tdc.pp()
tdc.stay(1)
tdc.stay(0)# STOP

tdc.stop()
tdc.reset()
tdc.start()
tdc.pp()

tdc.stop()
tdc.read()
tdc.reset()
tdc.start()

        
tdc.setSlow(0)

# osc.send('PACU 1,FREQ,C2')
# osc.send("PACU? 1")
osc.clearSweeps()
freq=osc.getMeasurement(1)

tdc.setFast(0b01111); tdc.send(); osc.send("CLSW"); osc.getMeasurement(1).AVG


date=time.strftime("%Y_%m_%d-%H_%M_%S"); jour, heure=date.split('-')
fout=open("tdc_"+date+".log", "w") ;fout.write("#FAST freq\n")

code

for code in range(31):
    tdc.setFast(code); tdc.send(); osc.send("CLSW")
    fout.write("\n")
    while float(osc.getMeasurement(1).SWEEPS)<=100:
        None
    freq=osc.getMeasurement(1)
    msg=str(code)+"\t".join(freq.AVG, freq.SIGMA)
    print(msg)
    fout.write(msg+'\n')


fout.close()
print "splot '"+fout.name+"' u 1:2:($4-$3) w lp"
