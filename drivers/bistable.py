#!/usr/bin/env python
import smbus, time; from time import sleep
bus=smbus.SMBus(1); AT=0x27 # ls /dev/i2c-1  => smbus(1)
import RPi.GPIO as GPIO ; GPIO.setmode(GPIO.BOARD)


class bistable:
  filename="register.txt"
  
  def __init__(self, AT=0x27, gpio=[31,33,35,37]):
    self.version= "ebecheto-v1"
    self.AT=AT
    self.gpio=gpio
    self.gpio.reverse()
    [GPIO.setup(i, GPIO.IN) for i in self.gpio]
    with open(self.filename, 'r') as f:
      line1=f.readline()
      line=line1 if line1!='' else '0b0'
      base=2 if line[0:2]=="0b" else 10
      ioss=int(line, base)
      ios=ioss if 0<=ioss<2**8 else 0
    self.reg=ios
  
  def __del__(self):
    FILE = open(self.filename,"w"); FILE.write("{}".format(self.reg)); FILE.close()
  
  def addreg(self, nb):
    self.reg |= (1<<nb)
  
  def send(self, onoff):
    ports=[self.reg, 0x00]
    if onoff:
      ports.reverse()
    bus.write_byte_data(self.AT, ports[0], ports[1] )
    
  def release(self):
    bus.write_byte_data(self.AT,0x00,0x00)# 750mA 'clac' des 4 relais
    
  def reset(self):
    self.reg=0
    
  def regs(self):
    return ["{}:{}".format(i, self.read(i)) for i in range(4)]
  
  def read(self, i):
    return GPIO.input(self.gpio[i])

  
  
