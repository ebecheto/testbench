#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import spidev
import RPi.GPIO as GPIO
import time


def WriteByte(val):
    for bit in bin(val)[2:].rjust(8,'0'):
        WriteBit(bit)

def WriteBit(bit):
    GPIO.output(MOSI, int(bit))
    PulseEnable()
    GPIO.output(MOSI, 0)

def ReadByte():
    time.sleep(0.005)
    nByte=GPIO.input(MISO)
    for i in range(7):
        PulseEnable()
        nByte = (nByte<<1) + GPIO.input(MISO)
    PulseEnable()
    return nByte

def Reset():
    GPIO.output(RST, 1)
    time.sleep(0.020)
    GPIO.output(RST, 0)
    time.sleep(0.020)

def PulseEnable():
    time.sleep(0.005)
    GPIO.output(SPI_CLK, 1)
    time.sleep(0.005)
    GPIO.output(SPI_CLK, 0)

def SpiWrite(addr, data):
    GPIO.output(SSN, 0)
    time.sleep(0.005)
    WriteByte(0x77) #Write order
    WriteByte(addr) #Wr_addr
    WriteByte(data) #Wr_data
    time.sleep(0.005)
    GPIO.output(SSN, 1)
    print "Write addr=",addr,"   data=",bin(data)[2:].rjust(8,'0')

def SpiRead(addr):
    GPIO.output(SSN, 0)
    time.sleep(0.005)
    WriteByte(0x72) #Read order
    WriteByte(addr) #Rd_addr
    readVal = ReadByte() #Read the answerval
    time.sleep(0.005)
    GPIO.output(SSN, 1)
    print "Read  addr=",addr,"   data=",bin(readVal)[2:].rjust(8,'0')
    return readVal
    

GPIO.setmode(GPIO.BCM)
SSN, MISO, MOSI, SPI_CLK, RST = 6, 9, 10, 11, 19
CLOCK_SC = 26

#Setup input pins
for pin in [MOSI,RST,CLOCK_SC,SPI_CLK]:
    GPIO.setup(pin, GPIO.OUT, initial = 0)

GPIO.setup(SSN, GPIO.OUT, initial = 1)

#Setup output pin
GPIO.setup(MISO, GPIO.IN)

#Create the clock
Clk=GPIO.PWM(CLOCK_SC,1000) #Freq=1kHz

#Start the clock
Clk.start(50)#Duty cycle

Reset()

##################################################################
### EDIT HERE TO CHANGE THE REGISTERS ######

data = 0b10011000 #bit 7 = 1, bit 0 = 0
data = 0x98

#Full write transaction
SpiWrite(addr=0x00, data=0b11000100)
SpiWrite(addr=0x01, data=0b11011111)
SpiWrite(addr=0x02, data=0b10100000)
SpiWrite(addr=0x03, data=0b00000100)
SpiWrite(addr=0x04, data=0b00000000)

#Full read transaction
SpiRead(addr=0x00)
SpiRead(addr=0x01)
SpiRead(addr=0x02)
SpiRead(addr=0x03)
SpiRead(addr=0x04)

###################################################################

time.sleep(0.05)
#Stop the clock
Clk.stop()

#GPIO.cleanup()

