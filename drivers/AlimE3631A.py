#! /usr/bin/python
# -*- encoding: utf-8 -*-

import serial, time

class AlimE3631A:
    """
    make sure I/O config button is set to RS-232 and not HPIB / 488
    I this example, I used a USB Serial Converter and a female-female
    cross cable
    Make sure your select the correct /dev/ttyUSBx 
    """
    
    def __init__(self, ser="/dev/ttyUSB0", br9600=9600):
        self.SERIALPORT = ser
        #SERIALPORT = "/dev/ttyUSB1"
        self.BAUDRATE = br9600
        self.ser = serial.Serial(self.SERIALPORT, self.BAUDRATE)
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_TWO
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = True
        self.ser.terminator = "\n"
        # CR=\c LF=\n CR+LF=\c\n
        self.ser.open()
        self.response = ""
        self.send("SYST:REM") #<== a refaire si on appuye sur bouton 'Local'
        time.sleep(0.2)#<== le passage en remote mets un peu de temps
        self.idn = self.send("*IDN?")
 
    def send(self,MESSAGE):
        try:
            self.ser.write(MESSAGE+"\r\n")
            time.sleep(0.2) #<== dont spam it
            # to send many command "CMD1;CMD2;CMD3;CMD4?"
            # if a query, stop sending commands
            
            if '?' in MESSAGE:
#                time.sleep(0.5) 0.2+0.3
                time.sleep(0.3)
                self.response=self.ser.readline().strip('\r\n')
                return self.response

        except serial.errno as e:
            self.ser.open()
            self.send(MESSAGE)

    def __del__(self):
        self.ser.close()


    def volts(self, nb=2):
        ch=('P6V', 'P25V', 'N25V')
        return [self.send("MEAS:VOLT? " + ch[i]) for i in range(nb)]
    def volt(self, nb=2):
        return ["{0:.2f}".format(float(i)) for i in self.volts(nb)]
    def Volt(self, nb=2):
        return [i+" V" for i in self.volt(nb)]

    def idcs(self, nb=2):
        ch=('P6V', 'P25V', 'N25V')
        return [self.send("MEAS:CURR:DC? " + ch[i]) for i in range(nb)]
    def idc(self, nb=2):
        return ["{0:.3f}".format(float(i)) for i in self.idcs(nb)]
    def Idc(self, nb=2):
        return [i+" A" for i in self.idc(nb)]

    # def power(self, nb=2):
    #     return ["{}V*{}A".format(self.volt(nb)[i], self.idc(nb)[i]) for i in range(nb)]
    def power(self, nb=2):
        ch=('P6V', 'P25V', 'N25V')
        return ["{:.3f}V*{:.3f}A".format(float(self.send("MEAS:VOLT? " + ch[i])), float(self.send("MEAS:CURR:DC? " + ch[i]))) for i in range(nb)]
#         return [j for i in range(nb) for j in self.send("MEAS:VOLT? " + ch[i]), self.send("MEAS:CURR:DC? " + ch[i])]


    def currents(self):# old one to remove later
        i1=self.send("MEAS:CURR:DC? P6V")
        i2=self.send("MEAS:CURR:DC? P25V")
        i3=self.send("MEAS:CURR:DC? N25V")
        return i1, i2, i3

    def current2(self):
        i1=self.send("MEAS:CURR:DC? P6V")
        i2=self.send("MEAS:CURR:DC? P25V")
        return i1, i2

    def RES(self):
        return self.send("MEAS:RES?").split(',')[2]

    def res2temp(self, r):
        return 6.76101314e-07*(r**3) + 7.62125457e-04*(r**2) + 2.38630456e+00*r - 2.46928114e+02

    def temp(self):
        return self.res2temp(float(self.RES()))
    def temps(self):
        return "{}".format(round(self.temp()))
    def Temps(self):
        return self.temps()+" °C"

    def TEMP2RES(self,T):
        return 100*(1+ 3.908e-3*T - 5.775e-7*T**2 + (0 if T > 0 else -4.183e-12)*(T-100)**3 )
    
    def temperature(self):
        """
        if the ohmmeter is connected to a pt100 probe, the temperature is
        calculate by dichothomy. Chosen precision : 0.01
        Valable pour keithley par pour alim agilent... branch driver ?
        """
        measure=float(self.RES())
        inf=-200; sup=850 ; temp=0; essai=100
        while abs(measure-essai)>=0.01:
            if essai>measure:
                sup=temp
            else:
                inf=temp
            temp=(sup+inf)/2.0
            essai=self.TEMP2RES(temp)
        return round(temp)


    def __del__(self):
        self.send("SYST:LOC")


if __name__ == '__main__':
    import readline, sys
    readline.parse_and_bind("tab: complete")
    port="0" if len(sys.argv)<=1 else sys.argv[1]
    tty="/dev/ttyUSB"+port
    print "== connecting to "+tty+" and purging possible errors =="
    ae =  AlimE3631A(tty, 9600)
    while not( '0,"No error"') in ae.send("SYST:ERR?"):
        print ae.response
    print """___exemple:___
             OUTPut ON
             ...
             SYST:ERR?
             APPLY? P6V
             *RST
             SYST:REM                #<== si appuie Store/Local ==> redo it
             MEASure:VOLTage:DC? P6V
             MEAS:VOLT?
             MEAS:CURR:DC? P6V
             MEAS:CURR:DC? P25V
             INST:SEL P6V         #<== appuye bouton +6V
             APPL P6V, 1.8, 1.0   #<== Set 1.8 volts / 1.0 amp to +6V output
             APPL P25V, 3.5, 1.0  #<== Set 3.5 volts / 1.0 amp to +25V output
            """
    print 'To (q)uit, type q\n'
    msg = "*IDN?"
    while msg != 'q':
        ae.send(msg)
        if '?' in msg:
            print ae.response
        msg = raw_input('>')
        print '>',msg,'<'
