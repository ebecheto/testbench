import MSO
osc = MSO.MSO('169.254.222.26'); print "Osc connected"
import numpy as np
self=osc

slot=1
self.send("CH{}:SV:STATE?".format(slot))
self.send("CH{}:SV:STATE ON".format(slot))
self.send('DATA:SOURCE CH{}_SV_NORMal'.format(slot))
# self.send('DATA:SOURCE?') #=>'CH1_SV_NORMAL'
# self.send('DATA:ENCdg?')# =>SFPBINARY OK
# self.send('WFMOutpre:BYT_Nr?')#=> 4 OK
# self.send("CH1:SV:STATE OFF")
# self.send('DATa:SOUrce:AVAILable?') #=>'CH1,CH4'
# self.send("CH1:SV:STATE ON") #=> 'CH1_SV_NORMAL' OK

# curve=self.send('CURVE?')
# recordLengthSTR = self.send('horizontal:mode:recordlength?')
# numPoints = int(self.send('WFMOutpre:NR_Pt?'))
# print("recordlength=" + recordLengthSTR+ ", numPoints=" + str(numPoints))  #=> recordlength=1250, numPoints=1901
# datas=np.frombuffer(curve,np.float32,numPoints)

self.send("WFMOutpre:ENCdg ASCii")
curve=self.send('CURVE?')
# np.fromstring(curve,float,numPoints, sep=',')
values = [float(i) for i in curve.split(',')]
datas=np.array(values)

# values = [float(i) for i in curve.split(',')]
# datas=np.array(values)
file="spectrumView1.dat"
np.savetxt(file, datas, delimiter="\n")
self.send('WFMOutpre:YUNIT?') #=> '"dBm"'

# [self.send("WFMOutpre:"+s+"?") for s in ["WFID", "NR_Pt", "Center Freq", "Span"]]
numPoints = int(self.send('WFMOutpre:NR_Pt?'))
["WFMOutpre:"+s+"?" for s in ["WFID", "NR_Pt", "Center Freq", "Span"]]
self.send('WFMOutpre:WFID?')#=>'"CH1_SV_NORMAL, 1902 points, Center Freq: 875.6884MHz, Span: 500MHz, FFTlength 0"'
self.send('WFMOutpre:NR_Pt?')#=> '1901'
#self.send('WFMOutpre:Center Freq?')
self.send('WFMOutpre:CENTERFREQuency?') #= '875.6884E+6'
self.send('WFMOutpre:Span?')  #=> 500.0000E+6'
MARKER=self.send("SV:MARKER:REFERence:FREQuency?") #=> '873.8463E+6'

YUNIT, XUNIT, XZERO, XINCR=[self.send("WFMOutpre:"+s+"?") for s in ["YUNIT", "XUNIT", "XZERO", "XINCR"]]
print YUNIT, XUNIT, XZERO, XINCR #=> "dBm" "Hz" 625.6884000E+6 263.1578947368421E+3

footer="old_term=GPVAL_TERM\nset term pngcairo font \"Sans,9\"\noutfile=file[0:strstrt(file, \".\")-1].\".png\"\nset output outfile; replot; pr \"[\".outfile.\"] saved\"\nset t old_term 0 font \"Sans,9\"; replot\n"

gpfile=file.split(".")[0]+".gp" #=> 'spectrumView1.gp'
f=open(gpfile, 'w')
header='set tics format "%.1s%c"'
header+='\n'+'set xtics right rotate by 45'
header+='\n'+'set ylabel "[".YUNIT."]"'
header+='\n'+'set xlabel "[".XUNIT."]"'
header+='\n'
[f.write("{}={}\n".format(s,self.send("WFMOutpre:"+s+"?"))) for s in ["YUNIT", "XUNIT", "XZERO", "XINCR"]] #OK
f.write(header)

# WFID=','.join((self.send('DATA:SOURCE?'), self.send('WFMOutpre:CENTERFREQuency?'), self.send('WFMOutpre:Span?'), self.send('WFMOutpre:NR_Pt?')))
WFID=self.send('WFMOutpre:WFID?')#=too verbose
WFID=','.join(WFID.split(',')[:-1])+"\"" # WARNING, remove last split take off last double quote
f.write("WFID="+WFID+"\n")
f.write("file='"+file+"'\n")
f.write("plot file u (XZERO+$0*XINCR):1 w lp t WFID\n")
xys=zip(self.send("SV:MARKER:PEAKS:FREQuency?")[1:-1].split(','), self.send("SV:MARKER:PEAKS:AMPLITUDE?")[1:-1].split(','))
for n, xy in enumerate(xys):
	f.write("xMK{}={} ;yMK{}={};".format(n+1,xy[0],n+1,xy[1]))
	f.write("set label {} gprintf(\"%.2s%c\",xMK{}) at xMK{},yMK{} left\n".format(n+1,n+1,n+1,n+1))

for n, xy in enumerate(xys):
	f.write("set label {} gprintf(\"%.2s%c\", {}) at {},{}  left\n".format(n+1,xy[0],xy[0],xy[1]))

#set label 2   at position, Yc left
#f.write("replot\n")
f.write(footer)
f.close()
print("gnuplot "+gpfile+" -")



