import DelayGeneratorGFT1004

# pul = DelayGeneratorGFT1004.DelayGeneratorGFT1004('192.168.0.43')
pul = DelayGeneratorGFT1004.DelayGeneratorGFT1004('169.254.222.43')
pul.send("DELAY? T1")
# TRIG? T1
TRIG T1 LSS;TRIG T1 SS1

delay=100#<== [ns] nanoseconde unit
pul.send("DELAY T1,{}".format(delay))
delay+=100
pul.setDelay(1,delay)

max=3000
step=100
nb=max/step

for i in range(nb+1):
    pul.setDelay(1,i*step)
    raw_input("{}/{} => {}[ns] delay. next={}".format(i, nb, i*step,i*(step+1)))



