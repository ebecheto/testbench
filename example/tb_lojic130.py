#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spidev, time, struct
from lmk_conf import *
#from lmk_conf2 import *

import os; from time import sleep
os.system("sudo dtparam spi=on") #<== enable spi

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
# spi.max_speed_hz=1000000 #<= 1M
# spi.lsbfirst = False


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
CS1, CS2, CS3, LMK, RST=0, 5, 6, 13, 19
ASIC=True
#GPIO.setup(CS1, GPIO.OUT)
[GPIO.setup(CS, GPIO.OUT) for CS in CS1, CS2, CS3, LMK, RST]
[GPIO.output(CS, 1) for CS in CS1, CS2, CS3]
# RESET ASIC SPI, trig on 'posedge'
# GPIO.output(RST,0)
# GPIO.output(RST,1)
# GPIO.output(RST,0)

# GPIO.output(CS3, 0)
# GPIO.output(CS3, 1)

# GPIO.output(CS,0)
# spi.xfer2([0b01110010, 0xaa])
# GPIO.output(CS,1)

# >>> bin(ord('w'))
# '0b1110111'
# >>> "0b{0:08b}".format(ord('w'))
# '0b01110111'
# >>> "0b{0:08b}".format(ord('r'))
# '0b01110010'



# def send(reg, data=0xfa, CS=CS1 ):
#     GPIO.output(CS,0)
#     spi.xfer2([0b01110010, reg, data])
#     GPIO.output(CS,1)

def send(reg, data=0xfa, CS=CS1 ):
    GPIO.output(CS,0)
    spi.xfer2([0b01110111])
    # GPIO.output(CS,1)
    # GPIO.output(CS,0)
    spi.xfer2([reg])
    # GPIO.output(CS,1)
    # GPIO.output(CS,0)
    spi.xfer2([data])
    GPIO.output(CS,1)
        

# def read(x, CS=CS1):
#     GPIO.output(CS,0)
#     spi.xfer2([0b01110111, x])
#     res=spi.readbytes(1)
#     GPIO.output(CS,1)
#     return res

# maybe xfer2 filled with 0x00, wil provok a read for the third byte, and return the value directly    spi.xfer2([0b01110111, x])
# spi.xfer2([0xb0, 0xD9, 0x00, 0x00]) gives four returned values; last two should be data/
# [A TESTER]

def read(x, CS=CS1):
    GPIO.output(CS,0);res=[]
    res.append(spi.xfer2([0b01110010]))
    # GPIO.output(CS,1)
    # GPIO.output(CS,0)
    res.append(spi.xfer2([x]))
    # GPIO.output(CS,1)
    # GPIO.output(CS,0)
    res.append(spi.xfer2([0x00,0x00]))
    GPIO.output(CS,1)
#    return res[2::]
    return res

# while 1:
#     send(0xaa)
#     r=read(1)
#     print r


# row="0b"+"".join([str(i) for i in tableau[12]])
# list(bytearray(struct.pack('<I', eval(row))))

# spi.xfer2(['0b10110111'])
# >>> spi.lsbfirst
# False #<= [OK] verif au scope   _|™|_|™™|_|™™™|_

import AlimE3631A
# [A COMMENTER S'il N'Y A PAS D'aLIM CONNECTé]
alim=AlimE3631A.AlimE3631A("/dev/ttyUSB0")
# [A COMMENTER S'il N'Y A PAS D'aLIM CONNECTé]

# from lmk_conf import *

# np.array(["0b"+"".join([str(i) for i in reg]) for reg in tableau]) #<= view

# reg=tableau[12]
# reg=tableau[24]
# row="0b"+"".join([str(i) for i in reg])  #<= '0b01010101010101010000000000000111'
# b8x4=list(bytearray(struct.pack('<I', eval(row))))   #<= [7, 0, 85, 85]
# b8x4=list(bytearray(struct.pack('>I', eval(row))))   #<= [85, 85, 0, 7]
# spi.xfer2(b8x4)
# GPIO.output(LMK,1)
# GPIO.output(LMK,0)

# [ AVERIFIER!!!!!!!] J'ai inversé des données à envoyer a cause de la commande struc.pack  <I, C'est >I qu'il faut prendre : 

def conf(regs, verb=False):
    k=0
    for reg in regs:
        k=k+1
        row="0b"+"".join([str(i) for i in reg])  #<= '0b01010101010101010000000000000111'
#        raw_input("WC: {:2}, {}, {}".format(k,row,alim.imA())) if verb else time.sleep(0.05)
        b8x4=list(bytearray(struct.pack('>I', eval(row))))
        spi.xfer2(b8x4)
        GPIO.output(LMK,1)
        GPIO.output(LMK,0)

#conf(tableau, 0) # <= non-verbeux avec ', 0'  #=> marche pas ? trop rapide ?
conf(tableau, 1) # <= non-verbeux avec ', 0'  #=> marche pas ? trop rapide ?

# conf([tableau[17]]) #<== Envoie la Write Commande 17 du tableau 

def reg2b(regList):
        return "0b"+"".join([str(i) for i in regList])

# sbit2b(tableau[13]) #=> '0b01010101010101010000000000001000'

def bit2Byte(row='0b01010101010101010000000000001000'):
    return list(bytearray(struct.pack('>I', eval(row))))

# bit2Byte() #=> [85, 85, 0, 8]
# bit2Byte(sbit2b(tableau[13])) #=> [85, 85, 0, 8]

def bytes2bit(by=[3,0,0,12]):
    return list("".join((["{:08b}".format(b) for b in by])))

# reg2b(bytes2bit())  #=>  '0b00000011000000000000000000001100'

# reg2b(bytes2bit(readLMK(13)))
# ["{:08b}".format(b) for b in readLMK(13)]

def printRegTab(tableau):
    print("WC means Write Cycle")
    tabList=["0b"+"".join([str(i) for i in reg]) for reg in tableau]
    for i, line in enumerate(tabList):
        print("WC{:2d}|{}|R{}|{}".format(i+1, line, eval(line)&0x1f, bit2Byte(line)))

printRegTab(tableau)


# ON OFF VERIF WITH BIT_ARRAY
["{:08b}".format(b) for b in [4,0,0,12]] #=>["{:08b}".format(b) for b in [4,0,0,12]]
on=list("".join((["{:08b}".format(b) for b in [4,0,0,12]]))) #=>['0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','0','0']
off=list("".join((["{:08b}".format(b) for b in [3,0,0,12]])))

# conf([on], 0)
# conf([off], 0)



# def readLMK(reg):
#         ret=spi.xfer2([0,reg,0,31,0,0,0,0])
#         GPIO.output(LMK,1)
#         GPIO.output(LMK,0)
# #        return ret[4::]
# # J'ai l'impression qu'il faut faire tomber les Chip Select avant de pousser les zeros de relecture
#         return ret


def readLMK(reg):
    # documentation says last 5 bit (adrres) are inconsistant => to removed, or lets put back the adress value
    spi.xfer2([0,reg,0,31])
    GPIO.output(LMK,1)
    GPIO.output(LMK,0)
    ret=spi.xfer2([0,0,0,0])
    # J'ai l'impression qu'il faut faire tomber les Chip Select avant de pousser les zeros de relecture. OUI
#    return ret[::-1] #<= bytes reversed car lecture MSB First. 
    return ret

#readLMK(13)



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

# # configurationdes bits des 8 registre de l'ASIC
# send(0,0b00010001, CS3)
# send(1,0b11000000, CS3)
# send(2,0b10111111, CS3)
# #send(3,0b00000101, CS3)
# send(3,0b00011101, CS3)
# send(4,0b10000000, CS3)
# send(5,0b11111111, CS3)
# send(6,0b11111111, CS3)
# send(7,0b11111111, CS3)


# for i in range(8):
#     print(read(i, CS3))

print "** QUIT() MADE exprès **"
quit();#<== stop python -i
GPIO.output(RST,0)
GPIO.output(RST,1)
GPIO.output(RST,0)
send(7,0b11111111, CS3)
read(7, CS3)


# while 1:
#     send(1,0b11000000, CS3)
#     r=read(1)
#     print r
