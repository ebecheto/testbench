#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket,sys
import collections

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
                tmp = self.s.recv(OscilloWavePro.BUFFER_SIZE)
                self.response = tmp[8:-1]
        except socket.error as e:
            self.connect()
            self.send(MESSAGE)


    def request(self, req):
        """
        convenient generic function send request return
        WARNING could not work for some specifics
        ie. #=>  request("C1:VDIV?") ==> C1:VDIV 20E-3 V => 20E-3
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

if __name__ == '__main__':    
    print("Si ca marche pas, un autre process doit etre en marche -> kill")
    ws = OscilloWavePro('192.168.0.45')
    print("Connected ?")
    print '____exemple:____\nC1:VDIV?\n'
    print 'to (q)uit type q\n'

    msg = "*IDN?"
    while msg != 'q':
        ws.send(msg)
        if '?' in msg:
            print ws.response
        msg = raw_input('>')
    ws.close()
