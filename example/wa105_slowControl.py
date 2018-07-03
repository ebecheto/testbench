#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spidev
import RPi.GPIO as io
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=500000 #<= 500k
spi.max_speed_hz=100000 #<= 100k
spi.max_speed_hz=10000 #<= 10k
#spi.max_speed_hz=4000 #<= 4k
spi.mode=0b10   #<== mode 2 for adg738  (falling edge)
#spi.mode=0     #<== mode 0 for adg714 [CHECK]  (falling edge)

RN, CS1, CS2, CS3 = 16, 33, 35, 37
io.setmode(io.BOARD)

def io_status():
    ios= [io.input(x) for x in CS1, CS2, CS3, RN]
    print ios
    print spi.mode, spi.max_speed_hz
    

[io.setup(p,io.OUT) for p in RN, CS1, CS2, CS3 ]
io.output(RN,1) #<= to enable the adg714

def send(i, CS):
    spi.mode=2 if (CS==CS1 or CS==CS2)  else True # adg731 mode
    spi.mode=0 if CS==CS3 else True #<= adg714 mode (falling edge)
    io.output(CS,0)
    spi.xfer2([i])
    io.output(CS,1)
#    spi.mode=2 if CS==CS3 else True
#<= back to adg731 mode

#example:
# send(0,CS1)  #<= active the pin1 of the mux selected by chip select 1
# send(31,CS2) #<= active the pin 32 of the mux selected by chip select 2
# send(0b11111111,CS3)
# 
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# [28, 29, 30, 31]


# CS3 config:
# MOSI| SCLK | RDIOD | ENA_board_5 | ENA_4 | ENA_3 | ENA_2 | ENA_1 | 
# should i reveerse it ?
# send(0b11111111,CS3)

enableASIC           = 0b0000000
disableASIC          = 0b00011111
enableASIC_Injection = 0b11000000
enableASIC_RDIOD     = 0b00100000

# send(enableASIC_Injection, CS3)
# send(disableASIC, CS3)
# send(enableASIC, CS3)


def stim(stim16=[0b10111111, 0b11111101]):
    """
    4 daisy chained ASIC
    """
    spi.mode=0
# io.output(RN,1) <== reset 
    spi.xfer2(stim16)
#    spi.mode=2

# # all ON
# stim([0b11111111, 0b11111111])
# stim([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])

# spi.mode=0
# io.output(CS3,0)
# spi.xfer2([0b11111111])
# io.output(CS3,1)
# spi.mode=2

# for i in range(32):
#     pin=i if i<16 else i+12
#     send(pin,CS1)
#     raw_input("inject to pin {}".format(pin))

def strip(CS):
    for i in range(20):
        pin=i if i<16 else i+12
        send(pin,CS)
        raw_input("inject to pin {}".format(pin))

def on():
    send(enableASIC, CS3)

def off():
    send(disableASIC, CS3)

def stimON():
    send(enableASIC_Injection, CS3)
    stim([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])

print "USAGE : "        
print "send(enableASIC_Injection, CS3)"
print "send(disableASIC, CS3)"
print "send(enableASIC, CS3) #<= + disable injection"
print "stim([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])"
print "strip(CS1) or strip(CS2)"


print "arret voulu"
quit()

# BIT BANG WORK-AROUND
import os, time
# os.system("lsmod|grep spi")

stimON()

send(enableASIC_Injection, CS3)
spi.close()
os.system("sudo modprobe -r spi_bcm2708")
time.sleep(0.1)


MOSI=19 # 10 BCM
SCLK=23 # 11 BCM
[io.setup(i, io.OUT) for i in MOSI, SCLK]
io.output(MOSI, 1)
#Rising edge should push a 1 in registers
io.output(SCLK, 0)
io.output(SCLK, 1)

# now push additionnal 64 bits = 4 Asic chained of 16-bit registers
for i in range(64):
    io.output(SCLK, 0)
    io.output(SCLK, 1)

io.output(SCLK, 0) #<= pull down the line

def BBoff():
    io.output(MOSI, 0)
    for i in range(64):
        io.output(SCLK, 0)
        io.output(SCLK, 1)
    io.output(SCLK, 0) #<= pull down the line

def BBon():
    io.output(MOSI, 1)
    for i in range(64):
        io.output(SCLK, 0)
        time.sleep(0.1)
        io.output(SCLK, 1)
    io.output(SCLK, 0) #<= pull down the line


io.cleanup()

os.system("sudo modprobe spi_bcm2708")
time.sleep(0.1)
spi.open(0,0)

RN, CS1, CS2, CS3 = 16, 33, 35, 37
io.setmode(io.BOARD)
[io.setup(p,io.OUT) for p in RN, CS1, CS2, CS3 ]
io.output(RN,1) #<= to enable the adg714
