#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket,sys,time
import collections



def closerVal(val, nlist=[0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]):
    """
    take the closer value 'floor' under the select value in the selected list
    returns the list (one under, closer, one above, value)
    used to select the calibre of the oscillo
    => closerVal(x)[0] => zoom in
    => closerVal(x)[2] => zoom out
    """
    i, closer =min(enumerate(nlist), key=lambda x:abs(x[1]-val))
    above = nlist[i+1] if i < len(nlist)-1 else nlist[-1]
    under = nlist[i-1] if i > 0 else closer
    return under, closer, above, val



class OscilloWavePro:
    Measure = collections.namedtuple('Measure',
        'SLOT TEXT AVG HIGH LAST LOW SIGMA SWEEPS')
        
    BUFFER_SIZE = 1024

    def __init__(self, ip='192.168.0.45', port=1861):
        self.name= "WavePro735Zi"
        self.ip=ip
        self.port=port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.response = ""
        self.response_header = None
        self.idn = self.send("*IDN?")
        

    def __del__(self):
        self.s.close()

    def close(self):
        del(self)

    def connect(self):
        self.s.connect((self.ip, self.port))

    def send(self,msg):
        TAILLE=len(""+msg)
        HEADER = "81"+"01"+"01"+"00"+ ("%08x" % TAILLE)
        HEADER = HEADER.decode('hex')
        try:
            self.s.send(HEADER+msg)
            if '?' in msg:
                tmp=''
                while(tmp[-1:]!='\n'):
                    tmp+= self.s.recv(self.BUFFER_SIZE)
                self.response = tmp[8:-1]
                return self.response
        except socket.error as e:
            self.connect()
            self.send(msg)
    def get(self):
        return self.s.recv(self.BUFFER_SIZE)

    def getVal(self, req):
        """
        convenient generic function send request return
        WARNING could not work for some specifics
        Work with ie. #=>  getVal("C1:VDIV?") ==> C1:VDIV 20E-3 V => 20E-3
        IndexError: list index out of range *ù$! peut arriver
        ==> lancer self.s.recv(self.BUFFER_SIZE))
        ==> lancer osc.s.recv(osc.BUFFER_SIZE)
        pour purger
        """
        self.send(req)
        ret=self.response.split(' ')[1]
        return float(ret)

    def pava(self,ps=("MIN", "MAX"), ch=1):
        """osc.pava(("MEAN",), 1) or osc.pava(("MEAN","MAX"), 1)
        """
        ret=self.send("C{}:PAVA? ".format(ch)+', '.join(ps)).split("PAVA ")[1]
        return [float(ret.split(p+',')[1].split(' ')[0]) for p in ps]
        # tmp=self.send("C{}:PAVA? ".format(ch)+', '.join(ps))
        # tmp=tmp.replace('MIN,', ' ').replace('MAX,', ' ').split(' ')
        # return [float(tmp[i]) for i in range(2,2*len(ps)+1,2)]

    def clearSweeps(self):
        self.send("CLSW")

    def setCaliber(self, ch, vdiv, offset=0):
        self.send("C{}:VDIV {}; C{}:OFST {}".format(ch, vdiv, ch, offset))

    def ymix(self, ch):
        tmp=self.send("C{}:PAVA? MIN, MAX".format(ch))
    #    tmp="C1:PAVA MIN,11E-3 V,OK,MAX,503E-3 V,OK"
        tmp=tmp.replace('MIN,', ' ').replace('MAX,', ' ').split(' ')
    # mini=float(tmp[2]); maxi=float(tmp[4])
        return [float(tmp[i]) for i in (2,4)]

    def getPmax(self, ch=1, NUM1=3, restore=False):
        self.clearSweeps()
        old_P = self.getMeasureSlot(1), self.getMeasureSlot(2) if restore else None
        self.setMeasureSlot(1, 'MIN, C{}'.format(ch))
        self.setMeasureSlot(2, 'MAX, C{}'.format(ch))
        NUM=0
        while NUM<NUM1 :
#            print "NUM {}, NUM1 {}".format( NUM, NUM1 )
            pmin = self.getMeasurement(1)
            NUM=pmin.SWEEPS
            pmax = self.getMeasurement(2)
        self.send(";".join(old_P)) if restore else None
        return [float(p.AVG) for p in (pmin, pmax)]

    def getFrame(self, ch=1, **kwargs):
        vdiv   = self.getVal("C{}:VDIV?".format(ch))
        offset = self.getVal("c{}:OFST?".format(ch))
        ymin, ymax=self.pava(("MIN", "MAX"),ch)
#        ymin, ymax=self.getPmax(ch , **kwargs)
        gmax =  4*vdiv-offset
        gmin = -4*vdiv-offset
        return vdiv, offset, ymin, ymax, gmax, gmin

    def setFrame(self, ch=1):
        vdiv, offset  = [self.getVal("C{}:".format(ch)+tata+"?") for tata in "VDIV","OFST"]
        ymin, ymax=self.pava(("MIN", "MAX"),ch)
        vdiv=(ymax-ymin)/6
        offset=-(ymax+ymin)/2
        return self.setCaliber(ch, vdiv, offset)
            
    def printScreen(self):
        """
        supposant que la print config est bien faite (sshfs par ex)
        SCreen DumP
        """
        self.send("SCDP")


    def setMeasureSlot(self, slot, measurecommand):
        """Crée une mesure sur l'oscillo (jusqu'à douze mesures différentes.
           slot: numéro de la mesure
           measurecommand: commande et ses paramètres (voir documentation
            cdn.teledynelecroy.com/files/manuals/wm-rcm-e_rev_d.pdf )
            osc.setMeasureSlot(4, "MAX,C1" )
            osc.setMeasureSlot(4, "DDLY, C1, C2")
           """
        self.send("PACU {0},{1}".format(slot, measurecommand))


    def getMeasureSlot(self, slot):
        self.send("PACU? {}".format(slot))
        return self.response
    
# si fait trop vite apres un clearsweep peur creer une lecture UNDEF ...
    def getMeasurement(self, slot):
        self.send("PAST? CUST, P{}".format(slot))
        #print( self.response)
        tmp = self.response.split(',')[1:]
        mes =  dict()
        mes['SLOT'] = int(tmp[0][1:])
        offset = tmp.index('AVG')
        mes['TEXT'] = ' '.join(tmp[1:offset])
        tmp = tmp[offset:]
        
        for i in range(0, len(tmp), 2):
            mes[tmp[i]] = tmp[i+1].split(' ')[0]

# si pas assez de mesures, la moyenne, le min et le max n'on pas beaucoup de sens,
# on prend pour tous la mesure unique (qui est dans LAST du coup)
        if mes['AVG'] == 'UNDEF':
            mes['AVG']  = mes['LAST']
            mes['LOW']  = mes['LAST']
            mes['HIGH'] = mes['LAST']
            
        return  OscilloWavePro.Measure(
                    SLOT = mes['SLOT'],
                    TEXT = mes['TEXT'],
                    AVG = mes['AVG'],
                    HIGH = mes['HIGH'],
                    LAST = mes['LAST'],
                    LOW =  mes['LOW'],
                    SIGMA = mes['SIGMA'],
                    SWEEPS = mes['SWEEPS'])

## added convienient  features
# setMaxFit(1,1,2)    # default
# setMaxFit(1,None,2) # default
# setMaxFit(NDIV=3)   # could be preferer
    def setMaxFit(self, CH=1, PX=None, NDIV=3, MAX="MAX", ZOOM=True):
        """
        Ajuste le maximum
        MAX could be also Amplitude if needed
        setMaxFit(1, 2, NDIV=0, MAX="AMPL")
        """
        PX=CH if PX is None else PX
        vdiv=self.getVal("C{}:VDIV?".format(CH))
        self.send("C{}:OFST {}".format(CH, -NDIV*vdiv))
        self.send("PACU {}, {}, C{};CLSW".format(PX, MAX, CH))
        ymax=float(self.getMeasurement(PX).AVG)
        while ymax < (1+NDIV)*vdiv:
            vdiv=closerVal(vdiv)[0]
            self.send("C{}:VDIV {}; C{}:OFST {}".format(
                        CH,    vdiv,CH,  -NDIV*vdiv))
            while float(self.getMeasurement(PX).SWEEPS) <= 2:
                pass
            ymax=float(self.getMeasurement(PX).AVG)

        while ymax>(3+NDIV)*vdiv:
            vdiv=closerVal(vdiv)[2]
            self.send("C{}:VDIV {}; C{}:OFST {}".format(
                        CH,    vdiv, CH, -NDIV*vdiv))
            while float(self.getMeasurement(PX).SWEEPS) <= 2:
                pass
            ymax=float(self.getMeasurement(PX).AVG)

        vdiv=self.getVal("C{}:VDIV?".format(CH))
        if ZOOM:
            vdiv=ymax/(2+NDIV)
            self.send("C{}:VDIV {}".format(CH, vdiv))
        return vdiv

    def saveCurve(self,CurvName="OUT", Curve=None):
        self.send("vbs 'app.SaveRecall.Waveform.SaveSource=\"{}\"'".format(Curve)) if Curve else None
        self.send("vbs 'app.SaveRecall.Waveform.TraceTitle=\"{}\"'".format(CurvName))
        self.send("vbs 'app.SaveRecall.Waveform.DoSave'")

    def optimizeCaliber(self, ch, start1VperDiv=False):#, nSweeps=0):
        """
        set vertical caliber and cursor of the given channel to use
        all the screen available for display.
        """
        NDIV = 6
   
        # we need to mesure min and max, but we save the current parameters
        # to restore them afterwards
        old_params = self.getMeasureSlot(1), self.getMeasureSlot(2)
        self.setMeasureSlot(1, 'MIN, C{}'.format(ch))
        self.setMeasureSlot(2, 'MAX, C{}'.format(ch))

        # start with cursor in the middle of the screen and 
        # a 1V/div caliber. The signal should hopefully fit on the screen.
        if start1VperDiv:
            vdiv = 1
            offset = 0
        else:
            vdiv = float(self.getVal("C{}:VDIV?".format(ch)))
            offset = float(self.getVal("c{}:OFST?".format(ch)))

        redo = True
        while (redo):
            self.setCaliber(ch, vdiv, offset) 
           # acq_ok = 0
           # while not acq_ok:
           #     self.send("INR?")
            #    acq_ok = int(self.response.split(' ')[1]) & 1
          
            # typical response
            #C1:PAVA MIN,11E-3 V,OK,MAX,503E-3 V,OK
           # tmp = self.response.split(',')
            self.send("CLSW;ARM;WAIT")
            ymin = float(self.getMeasurement(1).AVG) 
            ymax = float(self.getMeasurement(2).AVG)
            self.send("TRMD AUTO")

            self.send("C{}:PAVA? MIN, MAX".format(ch))
            tmp = self.response.split(',')
            ok = tmp[2]=='OK' and tmp[5]=='OK'

            old_vdiv = vdiv
            old_offset = offset
            vdiv = (ymax-ymin)/NDIV if ok else 1
            offset = -(ymin+ymax)/2 if ok else 0
            #print ymin, ymax, vdiv, old_vdiv

            redo = abs(old_vdiv - vdiv)/vdiv > 0.01

        # restore old parameters
        self.send(old_params[0])
        self.send(old_params[1])

    def avgs(self):
        measures=self.send("PAST? CUST, AVG").split('AVG,')[1].split(',')
        measures=[m.split(' V')[0].split(' S')[0] for m in measures]
        return measures

    def yfit(self,ch=1,**kwargs):
        vdivNotMin=True
        loop=0
        self.clearSweeps()
        vdiv, offset, ymin, ymax, gmax, gmin=self.getFrame(ch)
        if (ymin>gmax or ymax<gmin):
            loop+=1
            vdiv=closerVal(vdiv)[0]
            offset=0
            self.setCaliber(ch, vdiv, offset)
            ymin, ymax=self.pava(("MIN", "MAX"),ch)
            gmax =  4*vdiv-offset;        gmin = -4*vdiv-offset
        while ymax>=gmax: # TODO : traiter a part le cas ymax>=gmax and ymin>gmin
            loop+=1
            vdiv = closerVal(vdiv)[2]# closerVal((ymax-ymin)/NDIV)[0]
            # if ymin>gmin:# sinon on ne touche pas a offset
            #     offset=-ymin-3*vdiv
            self.setCaliber(ch,vdiv, offset)
            ymin, ymax=self.pava(("MIN", "MAX"),ch)
#            ymin, ymax=self.getPmax(ch, **kwargs)
            gmax =  4*vdiv-offset;        gmin = -4*vdiv-offset
        while ymin<=gmin:  # TODO : traiter a part le cas ymax<gmax and ymin<=gmin
            loop+=1
            vdiv = closerVal(vdiv)[2]# closerVal((ymax-ymin)/NDIV)[0]
            offset = 3*vdiv-ymax
            self.setCaliber(ch,vdiv, offset)
            ymin, ymax=self.pava(("MIN", "MAX"),ch)
#            ymin, ymax=self.getPmax(ch, **kwargs)
            gmax =  4*vdiv-offset;        gmin = -4*vdiv-offset
        while ((ymax-ymin)<2*vdiv and vdiv > 0.001 and vdivNotMin):
            loop+=1
            vdiv = closerVal(vdiv)[0]# closerVal((ymax-ymin)/NDIV)[0]
            offset = -(ymax+ymin)/2
            self.setCaliber(ch,vdiv, offset)
            vdivNotMin = True if vdiv == self.getVal("C{}:VDIV?".format(ch)) else False
            ymin, ymax=self.pava(("MIN", "MAX"),ch)
#            ymin, ymax=self.getPmax(ch, **kwargs)
            gmax =  4*vdiv-offset;        gmin = -4*vdiv-offset
        # final zoom when ymax and ymin are in the screen for sure:
        # vdiv, offset, ymin, ymax, gmax, gmin=getFrame(osc,ch)
        vdiv, offset, ymin, ymax, gmax, gmin=self.getFrame(ch, **kwargs)
        vdiv=(ymax-ymin)/6
        offset=-(ymax+ymin)/2
        self.setCaliber(ch,vdiv, offset)
        return loop

#__________________
        
    def zoomCalibre(self):
        vdiv=self.getVal("VDIV?")
        vdiv=closerVal(float(vdiv))[0]
        self.send("VDIV {}".format(vdiv))

    def unzoomCalibre(self):
        vdiv=self.getVal("VDIV?")
        vdiv=closerVal(float(vdiv))[0]
        self.send("VDIV {}".format(vdiv))
        
    def beep(self,N=2):
        [self.send("BUZZ BEEP") for i in range(N)]
    
    def setMaxZoom(self, CH=1, PX=None, ZM=2, NUM=2):
        """
        zoom to the parameter "ie maximum" between +/- sdev (SIGMA)
        Warning, OFFSET cannot be above 1V or under -1V. why ?...
        (I can hear the relay clicking , changing some param in the scope)
        if VDIV<=100mv .. pfff. give-up that function
        """
        PX=CH if PX is None else PX
        while float(self.getMeasurement(PX).SWEEPS) <= NUM:
            pass
        ret=self.getMeasurement(PX)
        self.send("C{}:VDIV {};C{}:OFST {}".format(
            CH, ZM*float(ret.SIGMA), CH, -float(ret.AVG)))


#USAGE for shell test (not import from python)
#python drivers/OscilloWavePro.py -ip '192.168.0.48'
if __name__ == '__main__':
    import readline
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', default='192.168.0.45')
    args = parser.parse_args()
    ip=args.ip
    print("Si ca marche pas, un autre process doit etre en marche -> kill")
    ws = OscilloWavePro(ip)
    print("Connected ?")
    print  """    ____exemple:____    respond
    C1:VDIV?       #<== Voltage / division of channel 1
    TDIV?          #<== time / division
    TDIV 1E-3      #<== above 50us allowed when SetMaximumMemory set!
    PAST? CUST,P1  #<== measure given by param 1 , mean, max, sdev...
    SCDP           #<== screen dump = save to file.png
    C1:OFfSeT?     #<== OFST, gives the offset of channel 1
    PACU? 1        #<== reply how is set the parameter 1
    C2:TRA OFF     #<== disable 'Trace On' for C2 curve
    F1:DEF?        #<== syntax definition of math function
    C1:ASET FIND   #<== put channel 1 in a window scale (offest and div)
    BUZZ BEEP; BUZZ BEEP #<== 2beep sound emitted by the scope
    # set manually a parameter then ask 'PACU? 1' what is the syntax
    PACU 3, DDLY, C1, C2 #<== set param 1 as the delay between ch1 and ch2
    VBS 'app.Acquisition.Trigger.C2.Level=0.055' #<== more advanced features
    vbs 'app.SystemControl.CloseDialog' #<== close the bottom panel if opened
    """
    print 'to (q)uit type q\n'

    msg = "*IDN?"
    while msg != 'q':
        ws.send(msg)
        if '?' in msg:
            print ws.response
        msg = raw_input('>')
    ws.close()
