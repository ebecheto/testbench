import MSO
osc = MSO.MSO('169.254.222.26'); print "Osc connected"
# osc.send('HEADer OFF')
# osc.send('VERBose OFF')

osc.send("MEASUrement?")
osc.send("MEASUrement:LIST?")# 'MEAS1,MEAS2,MEAS3,MEAS4'
osc.send("HORIZONTAL?")
osc.send("HORizontal:ACQDURATION?") #=> '400.0000E-9'
osc.send('HEADer ON')
osc.send("HORIZONTAL?")
osc.send('HEADer OFF')
osc.send("*IDN?")
osc.send("TIME?") #=> '"10:44:15"'
osc.send("ACQuire:NUMAVg?") #=> 16
osc.send("DCL") #=> Clear Device Output Queue 
osc.send("DATE?") #=> '"2021-12-21"'
osc.send("DISplay:GRAticule?") #=> GRID
osc.send("DISplay:STYle?") #=> VECTORS
osc.send("ACQuire:STATE?")
osc.send("ACTONEVent:SEARCH:ACTION:SAVEIMAGe:STATE?") #=> 0

osc.send("MEASUREMENT:MEAS1?")
osc.send("*OPC?")
osc.send("MEASUREMENT:MEAS1:RESUlts:CURRentacq:MEAN?")
osc.send("DESE 1")
osc.send("*ESE 1")
osc.send("*SRE 0")
osc.send("*OPC")
osc.send("BUSY?")


wave=osc.send('CURVE?') ##45000\x12<IGJLRP< ...\xb8\xb6\xb5\xc6
osc.send("FILESystem:CWD?") #=> '"C:"'
# equivalent to ls
osc.send("FILESystem:DIR?") #=> '"Applications","PICompatibility","Temp.png"'
# equivalent to ls -l
osc.send("FILESystem:LDIR?") #=> '"Applications;DIR;4096;2021-05-22;08:38:38","PICompatibility;DIR;4096;2021-05-22;08:38:40","Temp.png;FILE;233672;2021-12-21;09:52:09"'
osc.send("FILESystem:HOMEDir?") #=> '"C:"'
osc.send("FILESystem:READFile Temp.png") #=> rien
osc.send('FILESystem:READFile \"Temp.png\"') #=> rien
osc.send('FILESystem:READFile \"C:/Temp.png\"') #=> 

osc.send('FILESystem:COPy \"C:/Temp.png\", \"C:/Tmp.png\"')
osc.s.recv(osc.BUFFER_SIZE)

# recv deconne : 3 coups de retard
# The *WAI command forces completion of previous commands that generate
# an OPC message. No commands after the *WAI are processed before the OPC
# message(s) are generated
osc.send('*WAI') #=> dunno
osc.send('*BUSY?') #=> Blocking ?
osc.send('*ESR?') #=> 160 : Block data error

# ('Acquiring waveform.')
#dpo.timeout = 10000
osc.send('acquire:stopafter sequence')
osc.send('acquire:state on')
osc.send('*opc?') # => '1'
print('Waveform acquired.')
osc.send('DATA:SOURCE ?')
osc.send('DATA:SOURCE CH1')
osc.send('DATA:SOURCE CH1_SV_NORMal')
osc.send('DATA:ENCdg SFPBinary')
##dpo.write('WFMOutpre:BN_Fmt RI')
osc.send('WFMOutpre:BYT_Nr 4')
recordLengthSTR = osc.send('horizontal:mode:recordlength?')
numPoints = int(osc.send('WFMOutpre:NR_Pt?'))
print("recordlength=" + recordLengthSTR+ "numPoints=" + str(numPoints))

# Setting DATa:STARt to 1 and DATa:STOP to the record length will always return the entire waveform.
osc.send('DATa:STARt 1')
osc.send('DATa:STOP '+ str(numPoints))

osc.send('WFMOutpre:NR_Pt?') #=> '1' #<= bug non ?


yOffset = float(osc.send('WFMOutpre:YOFf?'))
yMult = float(osc.send('WFMOutpre:YMUlt?'))
yZero = float(osc.send('WFMOutpre:YZEro?'))
print('\t'.join(map(str,[yOffset, yMult, yZero ])))
print(osc.send('*ESR?'))
print(osc.send('allev?'))
curve=osc.send('CURVE?')

osc.send("CH1_SV_MAXHold")
osc.send('CURVE?')
osc.send("CH1_SV_AVErage")
osc.send("CH1_SV_MINHold")

osc.send('DATa:SOUrce:AVAILable?')
# => 'CH1,CH1_SV_BASEBAND_IQ,CH4,CH4_SV_BASEBAND_IQ,CH1_SV_NORMAL,CH4_SV_NORMAL'
osc.send('WFMOutpre?')
# '2;16;BIN;RP;INT;LSB;"Ch1, DC coupling, 100mV/div, 40ns/div, 5000 points, Sample mode";1;Y;LIN;"s";80.0E-12;12.187500E-12;2500;"V";15.6250E-6;0.0E+0;2.0000E-3;TIME;ANALOG;0.0E+0;0.0E+0;9.91E+37;1'
osc.send('HEADer ON;VERBose ON')
osc.send('WFMOutpre?')
osc.send('HEADer OFF;VERBose OFF')
osc.send('WFMOutpre:ASC_Fmt?')
osc.send('WFMOutpre:CENTERFREQuency?') #= >0.0E+0
osc.send('DATA:SOURCE CH1_SV_BASEBAND_IQ')
osc.send('WFMOutpre:DOMain?')  #=> TIME  ????
osc.send('DATA:SOURCE?')  #= >CH1_SV_BASEBAND_IQ'
osc.send('DATA:SOURCE CH1_SV_NORMal')
osc.send('WFMOutpre:DOMain?')  #=> 'FREQ' [OK]

osc.send("WFMOutpre:ENCdg ASCii")
osc.send("WFMOUTPRE:ENCDG?") #=> ASC
osc.send("WFMOutpre:NR_Pt?") #=> '1' ? pourquoi 1 seul point
osc.send("WFMOUTPRE:WFID?")
# :WFMOUTPRE:WFID "CH1_SV_NORMAL, 1901 points, Center Freq: 710.2895MHz, Span: 1.25GHz, FFTlength 0"'

WFID=osc.send("WFMOUTPRE:WFID?")
WFID.split(',')
numPoints=int(WFID.split(', ')[1].split(' ')[0])

osc.send('DATa:STOP '+ str(numPoints))
osc.send('CURVE?') #=> .... -82.3898,-81.2222  [BUG:pas bon ascii format] En fais si ! c'est en dbm (-80dbm),
osc.send('DATa:STOP?')#<= OK memorised

osc.send('DATA:ENCdg SFPBinary')
curve=osc.send('CURVE?')
import numpy as np
np.frombuffer(curve,np.float32,numPoints)
[print(data) for data in datas]
file="spectrumView.dat"
np.savetxt(file, datas delimiter="\n")
# MARCHE PAS, les DONNES SONT PAS BONNES :Encodage ?
# REDO avec ASCII

osc.send("WFMOutpre:ENCdg ASCii")
osc.send('HEADer OFF;VERBose OFF')
curve=osc.send('CURVE?')
# np.fromstring(curve,float,numPoints, sep=',')
values = [float(i) for i in curve.split(',')]
datas=np.array(values)
file="spectrumView.txt"
np.savetxt(file, datas, delimiter='\n')
osc.send('HEADer ON;VERBose ON')
osc.send("WFMOUTPRE?")
osc.send("SV:SPAN 100E6")
osc.send("SV:SPAN?")
osc.send("SV:RBWMode?")
osc.send("SV:MARKER:PEAKS:AMPLITUDE?") #=> rien
osc.send("SV:MARKER:PEAKS:FREQuency?") #=> rien
osc.send("SV:MARKER:PEAK:MAXimum?") #=> 5
osc.send("SV:MARKER:PEAK:STATE?") #=> 1 <=> ON
osc.send("SV:MARKER:PEAK:THReshold?") #=> -50.0 indicating that only peaks with an amplitude greater than -50 dBm qualify for peak marker placement.

osc.send("SV:MARKER:PEAKS?")
':SV:MARKER:PEAKS:AMPLITUDE "-49.7251930236816";FREQUENCY "719.2315789368422E+6"'
osc.send("SV:MARKER:PEAK:THReshold 40")
osc.send("SV:MARKER:TYPe?") #=> ABSOLUTE
# DELTA => dBc
osc.send("SV:MARKER:PEAK:EXCURsion?") #=> '30.0'
osc.send("SV:MARKER:PEAK:EXCURsion 25.0")
osc.send("SV:MARKER:PEAK:EXCURsion 12.0")
osc.send("SV:CH<x>:SELect:RF_MAXHold?") # :SV:CH1:SELECT:RF_MAXHOLD 0'
osc.send("SV:MARKER:PEAK:STATE?") #=> 1
osc.send("SV:MARKER:PEAK:STATE CH1") #dunno
osc.send("SV:MARKER:REFERence:FREQuency?")  #=> 0.0E+0 719.1263E+6
osc.send("SV:MARKERS?")
osc.send("SV:CH1:SELect:RF_MAXHold ON") #=> nice one : enveloppe
osc.send("SV:CH4:SELect:RF_MAXHold ON") #=> nice one : enveloppe
osc.send("SV:CH1:SELect:RF_NORMal?")
osc.send("SV:CH1:SELect:RF_PHASe?")  #phase versus time <=> TIE ?
osc.send("SV:CH1:SELect:RF_PHASe ON")  #phase versus time <=> TIE ?

osc.send("SV:CH1:SELect:RF_MINHold ON") #=> nice one : enveloppe
osc.send("CLEAR") # equivalent clrear sweep

osc.send("MEASUREMENT:MEAS1?")
osc.send("MEASU:MEAS1:SUBGROUP:RESUlts:ALLAcqs:MAXimum? \"OUTPUT1\"") # '1.1568259221627E-9'
osc.send("MEASU:MEAS1:SUBGROUP:RESUlts:ALLAcqs:POPUlation? \"OUTPUT1\"") # equivalent nb sweep
osc.send("MEASU:MEAS1:SUBGROUP:RESUlts:ALLAcqs:STDDev? \"OUTPUT1\"") 

osc.send("MEASU?")
osc.send("MEASUrement?")  # idem
osc.send("MEASUrement:LIST?")# osc.send("MEASUrement:LIST?")

# AVG HIGH LAST LOW SIGMA SWEEPS
list=["MEAN", "MAX", "MIN", "STDD", "POPU"]

self=osc
slot=1
[self.send("MEASU:MEAS"+str(slot)+":SUBGROUP:RESUlts:ALLAcqs:"+var+"? \"OUTPUT1\"") for var in list]


osc.getMeasurement(1)
