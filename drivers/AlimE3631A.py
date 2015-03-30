#! /usr/bin/python

import serial, time

class AlimE3631A:
    
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
        self.ser.open()
        self.response = ""
        self.send("SYST:REM")
        time.sleep(0.2)#<== le passage en remote mets un peu de temps

    def send(self,MESSAGE):
        try:
            self.ser.write(MESSAGE+"\r\n")
            if '?' in MESSAGE:
                time.sleep(0.5)
                self.response=self.ser.readline()
                return self.response

        except serial.errno as e:
            self.ser.open()
            self.send(MESSAGE)

    def __del__(self):
        self.ser.close()


if __name__ == '__main__':
    import readline
    readline.parse_and_bind("tab: complete")
    ae =  AlimE3631A("/dev/ttyUSB0", 9600)
    while ae.send("SYST:ERR?") !='+0,"No error"\r\n':
        print ae.response
    print """___exemple:___
             OUTPut ON
             ...
             SYST:ERR?
             APPLY? P6V
             *RST
             MEASure:VOLTage:DC? P6V
             MEAS:CURR:DC? P6V
             INST:SEL P6V         #<== appuye bouton +6V
             APPL P6V, 5.0, 1.0   #<== Set 5.0 volts / 1.0 amp to +6V output
            """
    print 'To (q)uit, type q\n'
    msg = "*IDN?"
    while msg != 'q':
        ae.send(msg)
        if '?' in msg:
            print ae.response
        msg = raw_input('>')
        print '>',msg,'<'
