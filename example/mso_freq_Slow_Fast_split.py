import MPTDC, AlimE3631A, OscilloWavePro, time, PulseGenerator81160A
from numpy import arange
#osc = OscilloWavePro.OscilloWavePro('169.254.222.45'); print "Osc connected"
osc = MSO.MSO('169.254.222.26'); print "Osc connected"

pul = PulseGenerator81160A.PulseGenerator81160A('169.254.222.52', 4000)
pul.send("*IDN?") # 'TEKTRONIX,AWG5204,B030758,FV:6.7.0235.0'
pul.send("AWGCONTROL:RMODE TRIGGERED")
tdc=MPTDC.MPTDC(0x74)

# CH1 == ROS == AWG OUTPUT1 == START == Slow osc.setMeasureSlot(1, 'FREQ,C1')
# CH4 == ROF == AWG OUTPUT2 == STOP  == Fast osc.setMeasureSlot(2, 'FREQ,C4')

code=0
code=31
codeF=31 #<= arrete Fast
codeF=0

for code in range(32):
    fout=open("MSO/freqS_{:02}.log".format(code), "w")
    tdc.setSlow(code);tdc.send();
    for codeF in range(32):
        tdc.setFast(codeF);tdc.send();
        tdc.stop(); tdc.start(); #<= no need to stop if in this case, yes for sync command
        osc.send("CLEAR"); pul.send("*TRG"), #<= no need though to reload, Yes ^ needed ^
        sweep2=osc.getMeasurement(4)[4]
        sweep1=osc.getMeasurement(2)[4]
        while not(float(sweep2)>=2000 or float(sweep1)>=2000):
            sweep2=osc.getMeasurement(4)[4]
            sweep1=osc.getMeasurement(2)[4]
        freq=osc.getMeasurement(4)
        freqF=osc.getMeasurement(2)
        # msg="\t".join([str(code), str(codeF), freq.AVG, freq.SIGMA, freqF.AVG, freqF.SIGMA])+'\n'
        msg="\t".join([str(code), str(codeF), freq[1], freq[3], freqF[1], freqF[3], ])+'\n'
        print(msg)
        fout.write(msg)
    fout.write('\n'); fout.close()


        
# freq=osc.getMeasurement(1)
# freqF=osc.getMeasurement(2)
# msg="\t".join([str(code), str(codeF), freq.AVG, freq.SIGMA, freqF.AVG, freqF.SIGMA])+'\n'
# print(msg)

# fout.write(msg)
#     fout.write('\n'); fout.close()


