import MPTDC, AlimE3631A, OscilloWavePro, time, PulseGenerator81160A, MSO
from numpy import arange
#osc = OscilloWavePro.OscilloWavePro('169.254.222.45'); print "Osc connected"
osc = MSO.MSO('169.254.222.26'); print "Osc connected"

pul = PulseGenerator81160A.PulseGenerator81160A('169.254.222.52', 4000)
pul.send("*IDN?") # 'TEKTRONIX,AWG5204,B030758,FV:6.7.0235.0'
pul.send("AWGCONTROL:RMODE TRIGGERED")
tdc=MPTDC.MPTDC(0x74)

# ROFast sur CH1
# ROSlow sur CH4
osc.send('MEASUrement:DELETEALL')

osc.send("MEASUREMENT:MEAS1:SOURCE CH1")
osc.send("MEASUREMENT:MEAS1:TYPE FREQUENCY")
osc.send("MEASUREMENT:MEAS2:SOURCE CH4")
osc.send("MEASUREMENT:MEAS2:TYPE FREQUENCY")

# osc.setMeasureSlot(1, 'FREQUENCY,CH1')
# osc.setMeasureSlot(2, 'FREQUENCY,CH4')

code=0
code=31
codeF=31 #<= arrete Fast
codeF=0

for code in range(31):
    fout=open("MSO/JAN/freqSF_{:02}.log".format(code), "w")
    tdc.setSlow(code);tdc.send();
    for codeF in range(31):
        tdc.setFast(codeF);tdc.send();
        tdc.stop(); tdc.start(); #<= no need to stop if in this case, yes for sync command
        osc.send("CLEAR"); pul.send("*TRG"), #<= no need though to reload, Yes ^ needed ^
        freq=osc.getMeasurement(2)
        freqF=osc.getMeasurement(1)
        avg1, sweep1=float(freq.AVG),float(freq.SIGMA)
        avg2, sweep2=float(freqF.AVG),float(freqF.SIGMA)
        while not(sweep2>2000 and sweep2<9.0E+37 and avg2<9.0E+37  and sweep1>2000 and sweep1<=9.0E+37 and avg1<9.0E+37):
            # sweep2=float(osc.getMeasurement(1).SIGMA)
            # sweep1=float(osc.getMeasurement(2).SIGMA)
            freq=osc.getMeasurement(2)
            freqF=osc.getMeasurement(1)
            avg1, sweep1=float(freq.AVG),float(freq.SIGMA)
            avg2, sweep2=float(freqF.AVG),float(freqF.SIGMA)
        print("POPU1={:.2}| POPU2={:.2} :".format(sweep1, sweep2)),
        msg="\t".join([str(code), str(codeF), freq.AVG, freq.SIGMA, freqF.AVG, freqF.SIGMA])+'\n'
#        msg="\t".join([str(code), str(codeF), freq[1], freq[3], freqF[1], freqF[3], freq[4], freqF[4]])+'\n'
#        raw_input(msg)
        print(msg),
        fout.write(msg)
    fout.write('\n'); fout.close()


        
# freq=osc.getMeasurement(1)
# freqF=osc.getMeasurement(2)
# msg="\t".join([str(code), str(codeF), freq.AVG, freq.SIGMA, freqF.AVG, freqF.SIGMA])+'\n'
# print(msg)

# fout.write(msg)
#     fout.write('\n'); fout.close()

from os import system
system("cd MSO/JAN/; ./gifit.sh; animate SFc.gif&")
