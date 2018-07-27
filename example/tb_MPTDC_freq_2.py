#slow oscillator
import MPTDC, AlimE3631A, OscilloWavePro, time
osc = OscilloWavePro.OscilloWavePro('169.254.222.45'); print "Osc connected"
tdc=MPTDC.MPTDC(0x77)
date=time.strftime("%Y_%m_%d-%H_%M_%S"); jour, heure=date.split('-')
fout=open("tdc_"+date+".log", "w") ;fout.write("#SLOW freq\n")
for code in range(30):
    tdc.setSlow(code); tdc.send(); osc.send("CLSW")
    fout.write("\n")
    while float(osc.getMeasurement(1).SWEEPS)<=100:
        None
    freq=osc.getMeasurement(1)
    msg="\t".join([str(code), freq.AVG, freq.SIGMA])
    print(msg)
    fout.write(msg+'\n')



fout.close()
print "splot '"+fout.name+"' u 1:2:($4-$3) w lp"
