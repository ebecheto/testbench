import MPTDC, AlimE3631A, OscilloWavePro, time, PulseGenerator81160A
osc = OscilloWavePro.OscilloWavePro('169.254.222.45'); print "Osc connected"
# lancer en tache de fond : python  ~/testbench/drivers/bypassPipe.py&
pul = PulseGenerator81160A.PulseGenerator81160A('169.254.222.46')
tdc=MPTDC.MPTDC(0x77)

tdc.stop();tdc.reset();tdc.start();
#WRITE
tdc.WBR=0;tdc.RO_STAY=1;tdc.setBits();tdc.setPort();tdc.send()

pul.senf("OUTPut2 ON;OUTPut ON")
time.sleep(1.8)
pul.senf("OUTPut2 OFF;OUTPut OFF")
tdc.WBR=1;tdc.RO_STAY=0;tdc.setBits();tdc.setPort();tdc.send()
#RESULT=tdc.spi.xfer2([0]*112)
tdc.read()

cnts=tdc.res2cnt()

mem=[int(x,2) for x in cnts]
PD_9_9a1=mem[0:8] # => [513, 0, 768, 320, 160, 64, 48, 20]
PD_8_9a1=mem[8:17]
# ...
osc.getMeasurement(2).AVG# 672.085E+6'# SLOW

osc.getMeasurement(4).AVG# '1.19082E-9'  # SLOW
osc.getMeasurement(4).AVG# '1.48738E-9'  # FAST
osc.getMeasurement(4).AVG# '1.062951E-9' # SLOW SEUL
osc.getMeasurement(4).AVG# '1.369073E-9' # FAST SEUL


# mercredi 1 août 2018, 13:46:03 (UTC-0200)
cnts=tdc.res2cnt()
mem=[int(x,2) for x in cnts]

mem=[513, 0, 768, 320, 160, 64, 48, 20, 10, 4, 3, 1, 768, 896, 769, 3, 512, 0, 384, 0, 768, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 511, 1023, 1023, 1023, 1023, 1023, 1023, 1023]
PD_9_9a1=mem[0:8] # => [513, 0, 768, 320, 160, 64, 48, 20]

