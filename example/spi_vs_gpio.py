

import spidev
import os
import time



os.system("sudo modprobe  spi-bcm2835")
# print "pause 2sec wait for modprobe init"
time.sleep(0.1)
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=100000 #<= 100k
# [hex(x) for x in spi.xfer([0xAA])]
res=spi.xfer([0xAA])
print "recieved : {}".format([hex(x) for x in res])

os.system("sudo modprobe -r spi-bcm2835")


os.system("sudo modprobe  spi-bcm2835")
# print "pause 2sec wait for modprobe init"
time.sleep(0.1)

spi.open(0,0)
spi.max_speed_hz=100000 #<= 100k
res=spi.xfer([0xAA])
print "recieved : {}".format([hex(x) for x in res])

# disable spi for bitbang purpose
os.system("sudo modprobe -r spi-bcm2835")

quit()

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.gpio_function(8)#<== 


ENA=27
RDIOD=22
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)#<== TAKE CHIP select priority => Warning
GPIO.setup(7, GPIO.IN)
GPIO.setup(RDIOD, GPIO.OUT)
GPIO.output(8,1) #<==
GPIO.input(7) #<==

GPIO.setup(8, GPIO.SPI)#<== back to normal config



#GPIO.output(ENA,1)   #<== disable the chip ==> power off


os.system("sudo modprobe  spi-bcm2835")
# print "pause 2sec wait for modprobe init"
time.sleep(0.1)

spi.open(0,0)
spi.max_speed_hz=100000 #<= 100k
res=0
res=spi.xfer([0xbb])
print "recieved : {}".format([hex(x) for x in res])
