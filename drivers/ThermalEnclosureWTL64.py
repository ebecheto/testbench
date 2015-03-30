
# -*- encoding: utf-8 -*-
"""
Module permettant de gérer le four WTL64 du labo élec.

Note: Pour utiliser le four via ce module, il faut être dans le même
sous réseau que celui-ci et qu'il soit configuré en mode de commande
externe (c.f. manuel)

Le module utilise le protocole ASCII-2 du WTL64 via une connection TCP
sur le port 2049. On suppose que l'adresse de bus de l'appareil  est 01.

date: 03/12/14
"""

import socket
import time

class ThermalEnclosureWTL64:
    # taille du buffer de reception (la réponse à la commande $01? est 
    # très longue)
    BUFFER_SIZE = 4096
    TCP_PORT = 2049
    BUS_ADD = '01'
    FORMAT = ("{:06.1f} "*3 + # Temp, Humid, Fan
             "0000.0 "*4 + # Unused
             "0{:b}{:b}0000000{:b}000000000000000000000") # start, humidity, comp air
    

    def __init__(self, ip):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, ThermalEnclosureWTL64.TCP_PORT))
        self.response = ''
        self.last_cmd = None
        
        # température
        self.tempNominal = None
        self.tempMesured = None
        # humidité
        self.humidNominal = None
        self.humidMesured = None
        # ventilateur
        self.fan = None
        # canaux numérique (c.f. manuel + réponse à '$01?\r' )
        self.start = None
        self.humidity = None
        self.compAir = None
        
        self.getState()
        
    def __del__(self):
        #self.start = False
        #self.setState()
        self.s.close()

    def getTemp(self):
        self.getState()
        return self.tempMesured

    def setTemp(self, temp):
        self.tempNominal=temp
        self.setState()
        
        
    def getState(self): # récupère l'état actuel du fou
        self.send('$'+ThermalEnclosureWTL64.BUS_ADD+'I\r')
        tmp = self.response.split(' ')
        self.tempNominal = float(tmp[0])
        self.tempMesured = float(tmp[1])
        # humidité
        self.humidNominal = float(tmp[2])
        self.humidMesured = float(tmp[3])
        # ventilateur
        self.fan = float(tmp[4])
        # canaux numérique (c.f. manuel + réponse à '$01?\r' )
        num_canal = tmp[14]
        self.start = bool(int(num_canal[1]))
        self.humidity =  bool(int(num_canal[2]))
        self.compAir =  bool(int(num_canal[10]))
        
    def setState(self): # met à jour les paramètres du four
        assert(-70. <= self.tempNominal <= +180.)
        assert(0. <= self.humidNominal <= +980.)
        assert(50. <= self.fan <= +100.)
        cmd = '$'+ThermalEnclosureWTL64.BUS_ADD+'E '
        cmd += ThermalEnclosureWTL64.FORMAT.format(
                   self.tempNominal, self.humidNominal, self.fan,
                   self.start, self.humidity, self.compAir)
        cmd += '\r'
        #print cmd
        self.send(cmd)
        
    def send(self, msg):
        # le four est lent, il ne faut pas le spammer de commande
        # si moins d'une seconde entre les deux waite 0.2
        if self.last_cmd is not None:
            while time.time() - self.last_cmd < 1.:
                time.sleep(0.2)
                
        self.s.send(msg)
        self.response = self.s.recv(ThermalEnclosureWTL64.BUFFER_SIZE)
        self.last_cmd = time.time()
        
    def __str__(self):
        self.getState()
        start = "ON" if self.start else "OFF"
        str_ =  "WTL64 ({}):\n".format(start)
        str_ += "\tNominal temperature {}\n".format(self.tempNominal)
        str_ += "\tMesured temperature {}\n".format(self.tempMesured)
        if self.humidity:
            str_ += "\tNominal humidity {}\n".format(self.humidNominal)
            str_ += "\tMesured humidity {}\n".format(self.humidMesured)
        else:
            str_ += "\tHumidity OFF\n".format(self.tempNominal)
        str_ += "\tFan {}\n".format(self.fan)
        
        str_ += "\tCompress air {}\n".format(self.compAir)
        
        return str_
        
if __name__ == '__main__':
    four = ThermalEnclosureWTL64('192.168.0.44')
    print four
    four.tempNominal = 18.
    four.start = True
    four.humidNominal = 10.
    four.humidity = True
    four.setState()
    while raw_input('>') != 'q':
        print four
        
    four.start = False
    four.setState()
    
