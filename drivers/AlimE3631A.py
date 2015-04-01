#! /usr/bin/python

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
        self.ser.open()
        self.response = ""
        self.send("SYST:REM") #<== a refaire si on appuye sur bouton 'Local'
        time.sleep(0.2)#<== le passage en remote mets un peu de temps

    def send(self,MESSAGE):
        try:
            self.ser.write(MESSAGE+"\r\n")
            time.sleep(0.2) #<== dont spam it
            # to send many command "CMD1;CMD2;CMD3;CMD4?"
            # if a query, stop sending commands
            
            if '?' in MESSAGE:
#                time.sleep(0.5) 0.2+0.3
                time.sleep(0.3)
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
