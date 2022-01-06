#!/usr/bin/env python

import socket,sys, errno
import collections
import numpy as np


class MSO:
    BUFFER_SIZE = 32*1024
    MEAS=["MEAN", "MAX", "MIN", "STDD", "POPU"]
    Measure = collections.namedtuple('Measure', 'SLOT TEXT AVG HIGH LAST LOW SIGMA SWEEPS')
    def __init__(self, ip, port=4000):
        self.name= "Agilent"
        self.ip=ip
        self.port=port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()#<== now and then, connect need if using send. Otherwise, use senf into opened fifo from bypassPipe.py
        self.response = ""
        self.idn = self.send("*IDN?")
        self.stdin  = None
        self.stdout = None

    def __del__(self):
        self.s.close()

    def connect(self):
        self.s.connect((self.ip, self.port))

    def send(self,MESSAGE):
        try:
            self.s.send(MESSAGE+"\n")
            self.response='no ?'
            if '?' in MESSAGE:
                tmp=''
                while(tmp[-1:]!='\n'):
                    tmp+= self.s.recv(self.BUFFER_SIZE)
                self.response = tmp[:-1]
                # ret=""
                # self.response = self.s.recv(self.BUFFER_SIZE)
            return self.response.strip('\n')
        except socket.error as e:
            self.connect()
            self.send(MESSAGE)


    def setMeasurement(self, slot, measurecommand):
	"""
            osc.setMeasureSlot(4, "MAX,C1" )# Lecroy
            osc.setMeasureSlot(4, "AMPLITUDE,CH1" )# Tektro
	"""
	type, source=measurecommand.split(',')
	self.send("MEASUREMENT:MEAS{0}:TYPE {1};MEASUREMENT:MEAS{0}:SOURCE {2}".format(slot, type, source))


    def getMeasurement(self, slot):
	mes =  dict()
	mes['TEXT']=''
        mes['TEXT'] += self.send("MEASUREMENT:MEAS{0}:SOURCE?".format(str(slot)))
        mes['TEXT'] += ","+ self.send("MEASUREMENT:MEAS{0}:TYPE?".format(str(slot)))
	mes['SLOT']=slot
	mes['SWEEPS']=self.send("MEASU:MEAS{0}:SUBGROUP:RESUlts:ALLAcqs:{1}? \"OUTPUT1\"".format(str(slot), "POPU"))
	mes['AVG']=self.send("MEASU:MEAS{0}:SUBGROUP:RESUlts:ALLAcqs:{1}? \"OUTPUT1\"".format(str(slot), "MEAN"))
	mes['HIGH']=self.send("MEASU:MEAS{0}:SUBGROUP:RESUlts:ALLAcqs:{1}? \"OUTPUT1\"".format(str(slot), "MAX"))
	mes['LOW']=self.send("MEASU:MEAS{0}:SUBGROUP:RESUlts:ALLAcqs:{1}? \"OUTPUT1\"".format(str(slot), "MIN"))
	mes['SIGMA']=self.send("MEASU:MEAS{0}:SUBGROUP:RESUlts:ALLAcqs:{1}? \"OUTPUT1\"".format(str(slot), "STDD"))
	mes['LAST']=self.send("MEASU:MEAS{0}:RESUlts:CURRentacq:{1}?".format(str(slot), "MEAN"))
	return MSO.Measure(**mes) #<== apply every elemet of the dictionnary to the tupple for name indexing
#	return self.Measure(**mes)
#	return mes

    def getMeasurements(self):
	slots=self.send("MEASUrement:LIST?")
	ret=[self.getMeasurement(s.replace('MEAS','')) for s in slots.split(',')]
	return ret

    def getSV(self, slot=1, file="spectrumView3.dat"):
        self.send("CH{}:SV:STATE?".format(slot))
        self.send("CH{}:SV:STATE ON".format(slot))
        self.send('DATA:SOURCE CH{}_SV_NORMal'.format(slot))
        self.send("WFMOutpre:ENCdg ASCii")
        curve=self.send('CURVE?')
        values = [float(i) for i in curve.split(',')]
        datas=np.array(values)
#        file="spectrumView1.dat"
        np.savetxt(file, datas, delimiter="\n")
        # YUNIT, XUNIT, XZERO, XINCR=[self.send("WFMOutpre:"+s+"?") for s in ["YUNIT", "XUNIT", "XZERO", "XINCR"]]
        # print YUNIT, XUNIT, XZERO, XINCR #=> "dBm" "Hz" 625.6884000E+6 263.1578947368421E+3
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
        WFID=self.send('WFMOutpre:WFID?')#=too verbose
        WFID=','.join(WFID.split(',')[:-1])+"\"" # WARNING, remove last split take off last double quote
        f.write("WFID="+WFID+"\n")
        f.write("file='"+file+"'\n")
        f.write("plot file u (XZERO+$0*XINCR):1 w lp t WFID\n")
        xys=zip(self.send("SV:MARKER:PEAKS:FREQuency?")[1:-1].split(','), self.send("SV:MARKER:PEAKS:AMPLITUDE?")[1:-1].split(','))
        for n, xy in enumerate(xys):
                f.write("set label {} gprintf(\"%.2s%c\", {}) at {},{}  left\n".format(n+1,xy[0],xy[0],xy[1]))
        #set label 2   at position, Yc left
        #f.write("replot\n")
        f.write(footer)
        f.close()
        print("gnuplot "+gpfile+" -")


    # def getMeasurement(self, slot):
    #     """
    # 	self.send("MEASU:MEAS1:SUBGROUP:RESUlts:ALLAcqs:MEAN? \"OUTPUT1\"")
    # 	self.send("MEASU:MEAS1:SUBGROUP:RESUlts:ALLAcqs:POPU? \"OUTPUT1\"")
    #     """
    #     # while(self.send("MEASU:MEAS"+str(slot)+":SUBGROUP:RESUlts:ALLAcqs:POPU? \"OUTPUT1\"")=='0'):
    #     #     print("DEBUG POPU")
    #     #     True
    #     return [self.send("MEASU:MEAS"+str(slot)+":SUBGROUP:RESUlts:ALLAcqs:"+m+"? \"OUTPUT1\"") for m in self.MEAS]




#  " PULS:TRAN2:TRA"

if __name__ == '__main__':    
    import readline
    readline.parse_and_bind("tab: complete")
    print 'Wait 8 seconds (slow to respond the 1st time)\n'
    osc = MSO('192.168.0.47', 5025)
    print '''____exemple:____
             OUTPUT ON
             OUTPUT?
             OUTPut2 OFF
             VOLT 1.2
             VOLT2?
             PULS:TRAN2 1.2e-6   #<= set leading edge to 1.2us
             PULS:TRAN2?         #<= gives the leading edge value
             PULS:TRAN2:TRA 1e-6 #<= set trailing edge to 1us
             OUTP2:COMP ON #<= Enable OUT2_ 'complementary'
             FREQ 1KHz'''
    print 'To (q)uit, type q\n'
    msg = "*IDN?"
    while msg != 'q':
        osc.send(msg)
        if '?' in msg:
            print osc.response
        msg = raw_input('>')

#A81.send("PULSe:POWer 1.2\n")
