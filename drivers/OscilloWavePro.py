#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket,sys
import collections



def closerVal(val, nlist=[0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]):
    """
    take the closer value 'floor' under the select value in the selected list
    returns the list (one under, closer, one above, value)
    used to select the calibre of the oscillo
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
        

    def __del__(self):
        self.s.close()

    def close(self):
        del(self)

    def connect(self):
        self.s.connect((self.ip, self.port))

    def send(self,MESSAGE):
        TAILLE=len(""+MESSAGE)
        HEADER = "81"+"01"+"01"+"00"+ ("%08x" % TAILLE)
        HEADER = HEADER.decode('hex')
        try:
            self.s.send(HEADER+MESSAGE)
            if '?' in MESSAGE:
                tmp = self.s.recv(self.BUFFER_SIZE)
                self.response = tmp[8:-1]
                return self.response
        except socket.error as e:
            self.connect()
            self.send(MESSAGE)


    def getVal(self, req):
        """
        convenient generic function send request return
        WARNING could not work for some specifics
        ie. #=>  getVal("C1:VDIV?") ==> C1:VDIV 20E-3 V => 20E-3
        IndexError: list index out of range *ù$! peut arriver
        ==> lancer self.s.recv(self.BUFFER_SIZE))
        ==> lancer osc.s.recv(osc.BUFFER_SIZE)
        pour purger
        """
        self.send(req)
        ret=self.response.split(' ')[1]
        return float(ret)


    def clearSweeps(self):
        self.send("CLSW")

            
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
            vdiv=self.send("C{}:VDIV {}".format(CH, ymax/(2+NDIV)))
        return vdiv


    def zoomCalibre(self):
        vdiv=self.getVal("VDIV?")
        vdiv=closerVal(float(vdiv))[0]
        self.send("VDIV {}".format(vdiv))

    def unzoomCalibre(self):
        vdiv=self.getVal("VDIV?")
        vdiv=closerVal(float(vdiv))[0]
        self.send("VDIV {}".format(vdiv))

    
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




if __name__ == '__main__':
    import readline
    print("Si ca marche pas, un autre process doit etre en marche -> kill")
    ws = OscilloWavePro('192.168.0.45')
    print("Connected ?")
    print  """    ____exemple:____    respond
    C1:VDIV?       #<== Voltage / division of channel 1
    TDIV?          #<== time / division
    PAST? CUST,P1  #<== measure given by param 1 , mean, max, sdev...
    SCDP           #<== screen dump = save to file.png
    C1:OFfSeT?     #<== OFST, gives the offset of channel 1
    PACU? 1        #<== reply how is set the parameter 1
    C2:TRA OFF     #<== disable 'Trace On' for C2 curve
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
