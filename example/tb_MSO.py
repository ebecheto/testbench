import MSO
osc = MSO.MSO('169.254.222.26'); print( "Osc connected")

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
osc.send('SYST:ERR?')


# ('Acquiring waveform.')
#dpo.timeout = 10000
osc.send('acquire:stopafter sequence')
osc.send('acquire:state on')
osc.send('*opc?') # => '1'
print('Waveform acquired.')
osc.send('DATA:SOURCE?')
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
osc.send("SV:CH1:SELTrace?")


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
osc.send("CLEAR") # equivalent clear sweep

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

osc.send("CUSTOMTABLE:LIST?") # 'NONE'
osc.send("DATa?") # 'REF1;ASCII;CH1;1;1901;1;MAX;1;1'
a=osc.send("CURVe?") #'76,75,74,75,76,76,75,74,74,73,64,43,14,-15,-35,-46,-51,-56,-61,-65,-67,-67,-68,-69,-70,-70,-69,-70, ....  ,41,11,-17'
len(a.split(',')) # 1901

with open('wave.txt', 'w') as f:
    f.write("\n".join(a.split(',')))

# gnuplot> plot 'wave.txt' w lp # [OK]

>>> osc.send("MEASUREMENT:MEAS1?")
'1000;0;0;PERIOD;2.0000;4.0000;NONE;10.0000E+6;NONE;10.0000E+6;1;0;DOUBLE;NONE;0.0E+0;0.0E+0;UNDEFINED;30.0000E-3;0.0E+0;HIGH;CH1;1;1.0000;0.0E+0;0;0;SAME;SAME;1.0000;1.0000;0.0E+0;0.0E+0;-1.0000;-1.0000;1.0000;1.0000;0.0E+0;0.0E+0;-1.0000;-1.0000;30.0000E-3;30.0000E-3;TENNINETY;TENNINETY;90.0000;90.0000;50.0000;50.0000;10.0000;10.0000;90.0000;90.0000;50.0000;50.0000;10.0000;10.0000;5.0000;5.0000;AUTO;AUTO;PERCENT;PERCENT;FORWARD;BOTH;SAMEAS;FORWARD;1;6;0.0E+0;1.0000E+6;HIGH;HIGH;LOW;NOMINAL;SAMEAS;BOTH;RISE;FIRST;RISE;BOTH;AUTO;-1.0000;1.0000;RECORD;1;0;50.0000E-6;NORMAL;2.5000E+9;AUTO;100.0000;DBM;FFT;1;1;1;1;1;1;1;1;0;AUTO;0.0E+0;10;2;REPEATING;AUTO;12.0000;12.0000;1.0000;0.0E+0;MANUAL;AUTO;TYPE1;1.0000E+6;1.0000E+6;700.0000E-3;PCIE_GEN1;2.5000E+9;"";2.5000E+9;NONE;EVERY;EDGE;MEAN;CONSTANTCLOCK;0;ALLBITS;1.0000;1;50.0000;50.0000;MEAN;"";0;"Period";CH1;CH2;CH3;CH4;CH5;CH6;CH6;CH6'

>>> mes=osc.send("MEASUREMENT:MEAS2?")
'1000;0;0;FREQUENCY;2.0000;4.0000;NONE;10.0000E+6;NONE;10.0000E+6;1;0;DOUBLE;NONE;0.0E+0;0.0E+0;UNDEFINED;30.0000E-3;0.0E+0;HIGH;CH1;1;1.0000;0.0E+0;0;0;SAME;SAME;1.0000;1.0000;0.0E+0;0.0E+0;-1.0000;-1.0000;1.0000;1.0000;0.0E+0;0.0E+0;-1.0000;-1.0000;30.0000E-3;30.0000E-3;TENNINETY;TENNINETY;90.0000;90.0000;50.0000;50.0000;10.0000;10.0000;90.0000;90.0000;50.0000;50.0000;10.0000;10.0000;5.0000;5.0000;AUTO;AUTO;PERCENT;PERCENT;FORWARD;BOTH;SAMEAS;FORWARD;1;6;0.0E+0;1.0000E+6;HIGH;HIGH;LOW;NOMINAL;SAMEAS;BOTH;RISE;FIRST;RISE;BOTH;AUTO;-1.0000;1.0000;RECORD;1;0;50.0000E-6;NORMAL;2.5000E+9;AUTO;100.0000;DBM;FFT;1;1;1;1;1;1;1;1;0;AUTO;0.0E+0;10;2;REPEATING;AUTO;12.0000;12.0000;1.0000;0.0E+0;MANUAL;AUTO;TYPE1;1.0000E+6;1.0000E+6;700.0000E-3;PCIE_GEN1;2.5000E+9;"";2.5000E+9;NONE;EVERY;EDGE;MEAN;CONSTANTCLOCK;0;ALLBITS;1.0000;1;50.0000;50.0000;MEAN;"";0;"Frequency";CH1;CH2;CH3;CH4;CH5;CH6;CH6;CH6'


self=osc
self.send("MEASU:MEAS2:SUBGROUP:RESUlts:ALLAcqs:POPU? \"OUTPUT1\"")
# screenDump
osc.send("SAVE:IMAGE \"C:/Dut12_tests.png\"")
osc.send("SAVe:IMAGe:VIEWTYpe?") # 'FULLSCREEN'

osc.send("MEASUrement:ADDMEAS TIE") #<= what does that do?
osc.send("MEASUrement:LIST?") #=> add MEAS5 with TIE
osc.send("SAVe:REPOrt:COMMents?") # ?
osc.send("SAVe:EVENTtable:MEASUrement \"TEK000.CSV\"")
osc.send("FILESystem:DIR?")
osc.send("MEASUREMENT:MEAS1:SOURCE?") #=> CH1
osc.send("MEASUREMENT:MEAS1:TYPE?")   #=> 'PERIOD'
osc.send("MEASUREMENT:MEAS1:RESUlts:CURRentacq:MEAN?") #=> '1.1425302202128E-9'
osc.send("MEASUREMENT:MEAS1:RESUlts:CURRentacq?") #<= failed : marche pas, pas prévu

osc.send("MEASUREMENT:MEAS1:RESUlts?")

osc.getMeasurement(1)

self=osc
slots=self.send("MEASUrement:LIST?")

dct_arr=osc.getMeasurements()


import yaml #pip install pyyaml
import json
print(json.dumps(dct_arr, sort_keys=False, indent=4)) # bof

print(yaml.dump(dct_arr, sort_keys=False, default_flow_style=False))
import pprint

from tabulate import tabulate # pip install tabulate
import pandas as pd
df = pd.DataFrame(dct_arr)
print(tabulate(df.T, headers="keys"))
print(tabulate(df, headers="keys"))
#       SLOT  TEXT                    AVG         HIGH          LAST           LOW        SIGMA     SWEEPS
# --  ------  -------------  ------------  -----------  ------------  ------------  -----------  ---------
#  0       1  CH1,AMPLITUDE   0.578542     0.597568      0.578351      0.559334     0.00439924     4378142
#  1       2  CH1,FREQUENCY   8.74329e+08  8.84938e+08   8.74945e+08   8.60892e+08  2.18675e+06  437555451
#  2       3  CH4,PERIOD      1.1425e-09   1.16057e-09   1.14223e-09   1.1283e-09   2.41023e-12  437412643
#  3       4  CH4,FREQUENCY   8.75277e+08  8.86288e+08   8.75972e+08   8.61642e+08  1.84549e+06  437412817
#  4       5  CH4,TIE        -1.94855e-26  2.00375e-11  -5.33954e-23  -1.89324e-11  3.06471e-12   49572967

pd.DataFrame(dct_arr)#<== suffit pour affichage

pip install si-prefix
from si_prefix import si_format
print si_format(.5)
# 500.0m  (default precision is 1)
type(si_format(.5))
df.applymap(si_format)

def is_float(element: Any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


lambda x: str(x).replace('.','').isdigit()).any()
df.applymap(lambda x: str(x).replace('.','').isdigit())

import si_prefix
si_prefix.SI_PREFIX_UNITS="yzafpnum kMGTPEZY"

def siSuffixNotation(element):
    try:
        ret=float(element)
        return str(si_format(ret)).replace(' ','')
    except ValueError:
        return element

# bof, si_format renvoie de l'unicode, et mets un espace entre le chiffre et l unite
# solved with SI_PREFIX_UNITS="yzafpnum kMGTPEZY" and replace

df.applymap(siSuffixNotation)
#osc.send("MEASUREMENT:DELETE \"MEAS5\"")
# df=pd.DataFrame(osc.getMeasurements())
# df.applymap(siSuffixNotation)



slot=1
self=osc
osc.send("CH1:SV:STATE?")
osc.send("CH1:SV:STATE ON")
osc.send('DATA:SOURCE CH1_SV_NORMal')
# osc.send('DATA:SOURCE?')
# osc.send('DATA:ENCdg?')# =>SFPBINARY OK
# osc.send('WFMOutpre:BYT_Nr?')#=> 4 OK
# osc.send("CH1:SV:STATE OFF")
# osc.send('DATa:SOUrce:AVAILable?') #=>'CH1,CH4'
# osc.send("CH1:SV:STATE ON") #=> 'CH1_SV_NORMAL' OK


import numpy as np

curve=osc.send('CURVE?')
recordLengthSTR = osc.send('horizontal:mode:recordlength?')
numPoints = int(osc.send('WFMOutpre:NR_Pt?'))
print("recordlength=" + recordLengthSTR+ "numPoints=" + str(numPoints))
datas=np.frombuffer(curve,np.float32,numPoints)
# values = [float(i) for i in curve.split(',')]
# datas=np.array(values)
file="spectrumView1.dat"
np.savetxt(file, datas, delimiter="\n")
osc.send('WFMOutpre:YUNIT?') #=> '"dBm"'

# [osc.send("WFMOutpre:"+s+"?") for s in ["WFID", "NR_Pt", "Center Freq", "Span"]]
numPoints = int(osc.send('WFMOutpre:NR_Pt?'))
["WFMOutpre:"+s+"?" for s in ["WFID", "NR_Pt", "Center Freq", "Span"]]
osc.send('WFMOutpre:WFID?')#=>'"CH1_SV_NORMAL, 1902 points, Center Freq: 875.6884MHz, Span: 500MHz, FFTlength 0"'
osc.send('WFMOutpre:NR_Pt?')#=> '1901'
#osc.send('WFMOutpre:Center Freq?')
osc.send('WFMOutpre:CENTERFREQuency?') #= '875.6884E+6'
osc.send('WFMOutpre:Span?')  #=> 500.0000E+6'
MARKER=osc.send("SV:MARKER:REFERence:FREQuency?") #=> '873.8463E+6'

YUNIT, XUNIT, XZERO, XINCR=[osc.send("WFMOutpre:"+s+"?") for s in ["YUNIT", "XUNIT", "XZERO", "XINCR"]]
YUNIT, XUNIT, XZERO, XINCR #=> "dBm" "Hz" 625.6884000E+6 263.1578947368421E+3

gpfile=file.split(".")[0]+".gp" #=> 'spectrumView1.gp'


osc.getSV(1)
osc.getSV(1, "sv4.dat", True)


osc.send('DATA:SOURCE CH1_SV_MAX_HOLD')
np.savetxt("CH1_SV_MAX_HOLD", np.array([float(i) for i in osc.send('CURVE?').split(',')]), delimiter='\n')


osc.send('DATA:SOURCE CH1_SV_BASEBAND_IQ')
np.savetxt("CH1_SV_BASEBAND_IQ", np.array([float(i) for i in osc.send('CURVE?').split(',')]), delimiter='\n')


osc.send('DATA:SOURCE CH1')
np.savetxt("CH1", np.array([float(i) for i in osc.send('CURVE?').split(',')]), delimiter='\n')

osc.send('WFMOutpre?')
'2;16;ASC;RP;INT;LSB;"Ch1, DC coupling, 100mV/div, 10ns/div, 1250 points, Sample mode";1250;Y;LIN;"s";80.0E-12;39.687500E-12;625;"V";15.6250E-6;0.0E+0;0.0E+0;TIME;ANALOG;0.0E+0;0.0E+0;2.3750E+3;1'


osc.send("SAVe:EVENTtable:MEASUrement \"TEK000.CSV\"")
osc.send("FILESYSTEM:READFILE \"TEK000.CSV\""); filestring=osc.send("?") #<= get
osc.send("FILESystem:DIR?") #=> '"Applications","PICompatibility","Temp.png"'

table='TEK000.CSV'
osc.send("SAVe:EVENTtable:MEASUrement \""+table+"\"")
osc.send("FILESYSTEM:READFILE \""+table+"\"");
# filestring=osc.send("*IDN?") #<= get
import numpy as np
self=osc
filestring=self.s.recv(self.BUFFER_SIZE)
np.savetxt(file, filestring, delimiter="\n")

osc.send('DATA:SOURCE?')
osc.send('MEASUrement:ADDMEAS FREQUENCY')

osc.s.recv(osc.BUFFER_SIZE)
osc.s.recv(1024)
osc.s.recv(1)


self=osc

"""
IEEE 488.2 Common Commands
*LRN? #<= toot verbose, but nice to save state and reload state
"""
self.prout="".join([self.prout+cmd+" => "+self.send(cmd)+'\n' for cmd in ('*OPC?','*OPT?','*STB?','*ESR?')])
return self.prout

# python3 socket changed default 
# .encode()

.chunk_size

#osc.send('HCOPY:PORT DISK;HCOPY START;*OPC')
osc.send('BUSY?')
osc.send('*WAI')
osc.send('EVENT?')
osc.send("EVMSG?")
osc.send('DCL')
osc.send('*ESR?')

osc.send("FILESYSTEM:READFILE \"TEK000.CSV\"")
osc.send('*ESR?')
osc.send('allev?')

osc.send("FILESYSTEM:READFILE \"existePAS\"")
osc.bug()
osc.send("FILESYSTEM:READFILE 'TEK000.CSV'?")
osc.bug()
osc.send("FILESYSTEM:READFILE 'TEK000.CSV'")
osc.bug()
osc.send("FILESYSTEM:READFILE 'TEK000.CSV'")
osc.send("*TRG")
osc.send('allev?')

self=osc
type="FREQUENCY"
source="CH1"
slot=1
self.send("MEASUREMENT:MEAS{0}:SOURCE {2};MEASUREMENT:MEAS{0}:TYPE {1}".format(slot, type, source))
type="FREQUENCY"
source="CH4"
slot=2
self.send("MEASUREMENT:MEAS{0}:SOURCE {2};MEASUREMENT:MEAS{0}:TYPE {1}".format(slot, type, source))



self.send("MEASUREMENT:MEAS{0}:SOURCE?".format(slot, type, source))
self.send("MEASUREMENT:MEAS{0}:TYPE?".format(slot, type, source))

self.send("MEASUREMENT:MEAS1:SOURCE CH1")
self.send("MEASUREMENT:MEAS1:TYPE FREQUENCY")
self.send("MEASUREMENT:MEAS2:SOURCE CH4")
self.send("MEASUREMENT:MEAS2:TYPE FREQUENCY")
#self.send("MEASUREMENT:MEAS1:TYPE?")

osc.send("MEASUREMENT:DELETE MEAS1")

osc.send('DATA:SOURCE CH4')

osc.setMeasureSlot(5, "FREQUENCY,CH4" )# 


print('***** Measurement List:')
print(osc.send('MEASUrement:LIST?'))

print('***** Value: PK2PK Measurement:')
print(osc.send('MEASUrement:MEAS1:VALUE?'))

print('***** Measurement with stats:')
print(osc.send('MEASUrement:MEAS1:RESULTS:ALLACQS:MEAN?;MINI?;MAX?;STDDEV?;POPU?'))

print('***** Measurement with unit and other tags:')
print(osc.send('MEASUrement:MEAS1:VALUE?;YUNIT?;TYPE?;SOUR1?;SOUR2?'))
osc.send('MEASUREMENT:MEAS1:SOURCE?')
