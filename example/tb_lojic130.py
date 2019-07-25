#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spidev,time
from lmk_conf import *


spi=spidev.SpiDev()
# import os; os.system("sudo modprobe  spi-bcm2835")
# print "pause 2sec wait for modprobe init"
# time.sleep(0.1)

spi.open(0,0)
#spi.max_speed_hz=27000000 #<= 27MHz
# spi.max_speed_hz=1000 #<== 1k
spi.max_speed_hz=100000 #<= 100k
#spi.max_speed_hz=500000 #<= 500k
#spi.mode=0b10 #<== mode 2 : Chip select Down, data on clock falling edge
#spi.max_speed_hz=1000000 #<= 1M
# spi.lsbfirst = False


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
CS1, CS2, CS3, LMK=0, 5, 6, 13
ASIC=True
[GPIO.setup(CS, GPIO.OUT) for CS in CS1, CS2, CS3, LMK]

# GPIO.output(CS,0)
# spi.xfer2([0b01110010, 0xaa])
# GPIO.output(CS,1)

# >>> bin(ord('w'))
# '0b1110111'
# >>> "0b{0:08b}".format(ord('w'))
# '0b01110111'
# >>> "0b{0:08b}".format(ord('r'))
# '0b01110010'



def send(reg, data=0xfa, CS=CS1 ):
    GPIO.output(CS,0)
    spi.xfer2([0b01110010, reg, data])
    GPIO.output(CS,1)
        

def read(x, CS=CS1):
    GPIO.output(CS,0)
    spi.xfer2([0b01110111, x])
    res=spi.readbytes(1)
    GPIO.output(CS,1)
    return res

# send(1)
# read(1)

# maybe xfer2 filled with 0x00, wil provok a read for the third byte, and return the value directly    spi.xfer2([0b01110111, x])
# spi.xfer2([0xb0, 0xD9, 0x00, 0x00]) gives four returned values; last two should be data/
# [A TESTER]
# def read(x, CS=CS1):
#     GPIO.output(CS,0)
#     res=spi.xfer2([0b01110111, x, 0x00, 0x00])
#     GPIO.output(CS,1)
#     return res[2::]



# row="0b"+"".join([str(i) for i in tableau[12]])
# list(bytearray(struct.pack('<I', eval(row))))

# spi.xfer2(['0b10110111'])
# >>> spi.lsbfirst
# False #<= [OK] verif au scope   _|™|_|™™|_|™™™|_

import AlimE3631A
alim=AlimE3631A.AlimE3631A("/dev/ttyUSB0")

# from lmk_conf import *
import struct
# np.array(["0b"+"".join([str(i) for i in reg]) for reg in tableau]) #<= view

# reg=tableau[12]
# reg=tableau[24]
# row="0b"+"".join([str(i) for i in reg])  #<= '0b01010101010101010000000000000111'
# b8x4=list(bytearray(struct.pack('<I', eval(row))))   #<= [7, 0, 85, 85]
# spi.xfer2(b8x4)
# GPIO.output(LMK,1)
# GPIO.output(LMK,0)


def conf(regs ):
    k=0
    for reg in regs:
        k=k+1
        row="0b"+"".join([str(i) for i in reg])  #<= '0b01010101010101010000000000000111'
        raw_input("reg{:2}, {}, {}".format(k,row,alim.imA()))
        b8x4=list(bytearray(struct.pack('<I', eval(row))))   #<= [7, 0, 85, 85]
        spi.xfer2(b8x4)
        GPIO.output(LMK,1)
        GPIO.output(LMK,0)

conf(tableau)

def readLMK(reg):
        ret=spi.xfer2([0,reg,0,31,0,0,0,0])
        GPIO.output(LMK,1)
        GPIO.output(LMK,0)
#        return ret[4::]
        return ret

readLMK(13)



# REGISTRE 12 : test LED LD_MUX of Ftest/LD pin
def lightOFF():
    GPIO.output(LMK,0)
    spi.xfer2([3,0,0,12]) #=>
    GPIO.output(LMK,1);GPIO.output(LMK,0)

def lightON():
    GPIO.output(LMK,0)
    spi.xfer2([4,0,0,12])
    GPIO.output(LMK,1);GPIO.output(LMK,0)

lightON()
lightOFF()
