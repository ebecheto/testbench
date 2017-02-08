#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spidev,time

spi=spidev.SpiDev()
import os; os.system("sudo modprobe  spi-bcm2835")
# print "pause 2sec wait for modprobe init"
time.sleep(0.1)

spi.open(0,0)
#spi.max_speed_hz=27000000 #<= 27MHz
spi.max_speed_hz=1000 #<== 1k
#spi.max_speed_hz=100000 #<= 100k
#spi.max_speed_hz=500000 #<= 500k
#spi.mode=0b10 #<== mode 2 : Chip select Down, data on clock falling edge
#spi.max_speed_hz=1000000 #<= 1M
# spi.lsbfirst = False

# import types
# isinstance(pow, types.BuiltinFunctionType)
# [eval( d + "()" if not isinstance(d,types.BuiltinFunctionType) else "") for d in dir(GPIO)]



import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
CS1, CS2, CS3=13, 19, 26
ASIC=True
[GPIO.setup(CS, GPIO.OUT) for CS in CS1, CS2, CS3]
#GPIO.setup(CS3, GPIO.OUT)
#GPIO.output(RDIOD,1) #<==
#GPIO.output(ENA,1)   #<== disable the chip ==> power off

def send(x, CS):
    spi.mode=0b10 if CS==CS1 or CS==CS2 or CS==CS3 else 0
    GPIO.output(CS,0)
    spi.xfer2([x])
    GPIO.output(CS,1)
#    spi.mode=0b0

send(0b11000000, CS3)
# enable all chip, and activate bus (Dzi, Dki) for ASIC config
# 1 chip has 16-channel => 0xFF,0xFF 
# chip     top ,2nd ,3rd , down
spi.mode=0
spi.xfer2([0xff,0Xff,0xff, 0xff,0xff,0Xff,0xff, 0xff])
spi.xfer2([0xFF for i in range(8)]) #<== CSTIM ALL
spi.xfer2([0 for i in range(8)])    #<== disabl calibration injection



send(0b00111111, CS3)#<== disable <=> !enable[1-5]

print "quit made on purpose\n" #quit()
print "Now use: \nsend(0b11000000, CS3)#<== to enable it again"
print "send(0b00111111, CS3)#<== to disable it ALL\n"
raise SystemExit()



spi.xfer2([31])
spi.xfer2([0xFF])

# #[spi.xfer2([i]) for i in range(17)]
# for i in range(32):
#     spi.xfer2([i])
#     print i
#     time.sleep(0.1)



#[spi.xfer2([i]) for i in range(17)]
for i in range(32):
    null=spi.xfer2([i])
    null=raw_input("[{}]next:1".format(i))

# ___________________________________________________________________________
# >>> ord('a')  ## chr(ord('a')+4)
# 97
# >>> hex(ord('a'))
# '0x61'
# >>> bin(ord('a'))
# '0b1100001'
# for i in range(7):
#     print bin(1<<i).zfill(8)
#'{:08b}'.format(7)

# n=1<<10
# print n, ~n, bin(~n&0xFFFF)


disableOne=[]
for i in range(64):
    nbit=~(1<<i)&0xFFFFFFFFFFFFFFFF
    print "{:2}".format(i), bin(~(1<<i)&0xFFFFFFFFFFFFFFFF), nbit
    disableOne=disableOne+[nbit]

# disableOne[::-1]#<== reverse list construct
b=disableOne[::-1]
test=disableOne[2]
test=b[2]


bin(test)
hash8rev=[]
for i in [8*i for i in range(8)]:
    hash8rev=hash8rev+[(test>>i)&0xFF]
    print bin((test>>i)&0xFF),

hash8=hash8rev[::-1]

spi.xfer2[hsh8]
