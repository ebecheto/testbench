import MPTDC, AlimE3631A, OscilloWavePro, time
osc = OscilloWavePro.OscilloWavePro('169.254.222.45'); print "Osc connected"
tdc=MPTDC.MPTDC(0x77)
date=time.strftime("%Y_%m_%d-%H_%M_%S"); jour, heure=date.split('-')
fout=open("tdc_"+date+".log", "w") ;fout.write("#FAST freq\n")

fout.write("# "+"\t".join(["code","code2", "per1.AVG", "per1.SIGMA", "per2.AVG", "freq2.SIGMA", "freq1.AVG", "freq1.SIGMA", "freq2.AVG", "freq2.SIGMA"])+"\n")

for code in [15, 23, 27, 29, 30, 7, 11, 19, 13, 14, 21, 22, 25, 26, 3, 28, 5, 9, 6, 10, 17, 12, 18, 20, 24, 1, 2, 4, 8, 16, 0]:
    tdc.setFast(code)
    for code2 in range(31):
        tdc.setSlow(code); tdc.send(); osc.send("CLSW")
        while float(osc.getMeasurement(1).SWEEPS)<=100:
            None
        per1=osc.getMeasurement(3)
        per2=osc.getMeasurement(4)
        freq1=osc.getMeasurement(1)
        freq2=osc.getMeasurement(2)
        msg="\t".join([str(code),str(code2), per1.AVG, per1.SIGMA, per2.AVG, freq2.SIGMA, freq1.AVG, freq1.SIGMA, freq2.AVG, freq2.SIGMA])
        print(msg)
        fout.write(msg+'\n')


fout.close()
print "splot '"+fout.name+"' u 1:2:($4-$3) w lp"
