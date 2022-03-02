import MPTDC, AlimE3631A, OscilloWavePro, time

osc = OscilloWavePro.OscilloWavePro('169.254.222.45'); print "Osc connected"

tdc=MPTDC.MPTDC(0x77)

tdc.pp()
tdc.stay(1)
tdc.stay(0)# STOP

tdc.stop()
tdc.reset1()
tdc.start()
tdc.pp()

tdc.stop()
tdc.read()
tdc.reset()
tdc.start()

tdc.RST=0
tdc.setBits()
tdc.send()

tdc.stop();tdc.reset();tdc.start();tdc.read1()

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



import PulseGenerator81160A;
pul = PulseGenerator81160A.PulseGenerator81160A('169.254.222.46')

#tdc.spi.max_speed_hz=100000

tdc.stop();tdc.reset();tdc.start();
#WRITE
tdc.WBR=0;tdc.RO_STAY=1;tdc.setBits();tdc.setPort();tdc.send()

pul.senf("OUTPut2 ON;OUTPut ON")
time.sleep(1.8)
pul.senf("OUTPut2 OFF;OUTPut OFF")
tdc.WBR=1;tdc.RO_STAY=0;tdc.setBits();tdc.setPort();tdc.send()
RESULT=tdc.spi.xfer2([0]*112)



tdc.check()

RESULT=[31, 251, 255, 191, 235, 253, 127, 207, 251, 254, 191, 215, 252, 255, 63, 239, 254, 127, 63, 63, 255, 255, 255, 255, 255, 247, 255, 255, 255, 159, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# tdc.res2cnt() # RESULTS -> binary 112x11-bit counter list


[int(x,2) for x in self.counters]
