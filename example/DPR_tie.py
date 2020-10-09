#! /usr/bin/python

import AlimE3631A, OscilloWavePro, time; from numpy import arange
osc = OscilloWavePro.OscilloWavePro('192.168.0.45'); print "Osc connected"
alim=AlimE3631A.AlimE3631A("/dev/ttyUSB0")

res=alim.send("*IDN?")
print "Response : ["+res+"]"

# res=alim.send("APPL P6V, 1.8")

freq=osc.getMeasurement(8)
freq.SIGMA
# osc.send("SCDP")

codes=arange(0.4, 1.0, 0.005)

# https://teledynelecroy.com/doc/using-python-with-activedso-for-remote-communication
# Set app = CreateObject("LeCroy.XStreamDSO")
osc.send("VBS app.Measure.ShowMeasure = true")
# >>> osc.send("VBS app.Measure.ShowMeasure = false")
# >>> osc.send("VBS? 'return=app.Measure.ShowMeasure'")
# 'VBS 0'
osc.send("VBS app.Measure.ShowMeasure = true")
# >>> osc.send("VBS? 'return=app.Measure.ShowMeasure'")
# 'VBS -1'
osc.send("VBS? 'return=app.Measure.P1.Out.Result.Value' ")#'VBS No Data Available'
osc.send("VBS? 'return=app.Measure.P1.sdev.Result.Value' ")# 'VBS 3317668.96032874'
osc.send("vbs 'app.SDA.Htie.Out.Result'")
osc.send("vbs? 'return=app.SDA.TIETrend.Out.Result'")# <= get Rj Pj and Dj ?
osc.send("vbs 'app.SystemControl.CloseDialog'")
osc.send("vbs? 'return=app.Display.Persisted'")
osc.send("VBS? 'return=app.Measure.P1.Out.Result.Value'")# => 'VBS No Data Available'
osc.send("VBS? 'return=app.measure.p1.mean.result.value'") #=> 'VBS 78933.5583985242'
osc.send("vbs? 'return=app.SDA.TIETrend.mean.Result.value'")# <= get Rj Pj and Dj ?
osc.send("vbs? 'return=app.Utility.DateTimeSetup.CurrentDateAndTime")
#=> 'VBS Tuesday, October 06, 2020 9:45:55 PM'
osc.send("vbs? 'return=app.Acquisition.C2.VerScale'")
osc.send("VBS? 'return=app.PMA.Class'")# marche pas
osc.send("vbs? 'return = app.InstrumentModel ")#=> 'VBS WP735Zi'
# remarque : pas besoin de la dernière quote ?§§!?
osc.send("vbs? 'return = app.Acquisition.TriggerMode'") #=> 'VBS Normal'
osc.send("vbs? 'return = app.Measure.P"+ "1"+ ".Out.Result.Value'")#=> 'VBS No Data Available' <=parametre pas actif
osc.send("vbs? 'return = app.Measure.P1.Equation'")#=> 'VBS freq(F1)'

for i in range(12):
    str(i+1)+"|" + osc.send("vbs? 'return = app.Math.F"+str(i+1)+".Operator1'")

for i in range(12):
    str(i+1)+"|" + osc.send("vbs? 'return = app.Math.F"+str(i+1)+".Equation'")

osc.send("vbs? 'return =  app.Math.F1.Out.Result.Samples")#'VBS 999999'
osc.send("vbs? 'return =  app.Math.F1.Out.Result.DataArray")
#=> 'VBS Cannot convert Variant to String'
osc.send("vbs? 'return =  app.Math.F1.Out.Result.DataArray(10,10,1,1)")


# osc.send("""VBS'app.Acquisition.C1.VDIV=".02V"'""",1)
osc.send("VBS? 'return=app.Measure.P1.Out.Result.Value'")#'VBS No Data Available'
osc.send("vbs? 'return=app.measure.p1.out.result.value'")#'VBS No Data Available'
osc.send("INSPECT? SIMPLE")
osc.send("INSPECT? SIMPLE, WORD")
osc.send("INSPECT? SIMPLE, FLOAT")
osc.send("INSPECT? DUAL")
osc.send("INSPECT? DATA_ARRAY_1")
osc.send("INSPECT? DATA_ARRAY_2")
osc.send("F3:WAVEFORM?")
osc.send("F3:INSP? TIMEBASE")
osc.send("TEMPLATE?")
osc.send("WFSUSP,3,FP,200")
osc.send("WAVEFORM_SETUP?")


# osc.get()
# osc.s.recv(osc.BUFFER_SIZE)
fout=open("jitterTie_fSeul_80M.log", "w") ;fout.write("#freq\tSigma\tVcontrol\n")
for code in codes:
    alim.send("APPL P6V, {}".format(code))
    osc.send("CLSW")
    while float(osc.getMeasurement(8).SWEEPS)<=100:
        None
    osc.send("SCDP")
    freq=osc.getMeasurement(6)
    jitt=osc.getMeasurement(8)
    msg=str(code)+"\t"+"\t".join([freq.AVG, jitt.SIGMA])
    print(msg)
    fout.write(msg+'\n')

fout.close()
print "plot '"+fout.name+"' u ($2*4):3 w lp"

# plot 'jitterTie_fSeul.log' u ($2*4):3 w lp
