#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spidev
import RPi.GPIO as GPIO
import os; from time import sleep
os.system("sudo dtparam spi=on") #<== enable spi
spi=spidev.SpiDev(); spi.open(0,0)
os.system("sudo dtparam spi=off") #<== disable spi => BITBANG possible
# print "pause 2sec wait for modprobe init" # time.sleep(0.1)

GPIO.setmode(GPIO.BCM)
CS1, CS2, CS3, LMK = 0, 5, 6, 13
MISO, MOSI, SPI_CLK = 9, 10, 11
RST=19; CLOCK_SC = 26
[GPIO.setup(CS, GPIO.OUT) for CS in CS1, CS2, CS3, LMK, RST, CLOCK_SC, MOSI,SPI_CLK]
GPIO.setup(MISO, GPIO.IN)

TAP=0.0001 #<= 100us .
GPIO.output(RST, 0); GPIO.output(RST, 1)#= RESET
GPIO.output(MOSI, 0)
GPIO.output(SPI_CLK, 0)
# Choix prendre CGIO26 pour CLOCK_SC_20MHz
GPIO.output(CLOCK_SC, 0)
# GPIO.input(MISO)

def fsmup(nb=1):
    for i in range(nb):
        GPIO.output(CLOCK_SC, 1)
        sleep(TAP)
        GPIO.output(CLOCK_SC, 0)
        sleep(TAP)

def up():
    GPIO.output(SPI_CLK, 1)
    sleep(2*TAP)

def down():
    GPIO.output(SPI_CLK, 0)
    sleep(2*TAP)

# fsmup(1)
# fsmup(20)

MEM=0
def read(MEM,i=0):
    bit=GPIO.input(MISO)
    MEM = MEM | (bit<<i) if bit else MEM & ~(1<<i)&0xff
    return MEM

#data=0xfa
send(0,0b00010001, CS3)
reg = 0 # 0xff : valeur sur 8 bits
data=0b00010001 #valeur sur 8 bits
              _
i=0


def envoie_8b(data, MEM=0):
    #<= ici data sera 'reg' ou 'data' ou 'w' ou 'r' , "c'est selon"
    for i in range(8):
        up() # SPI_CLK passe à 1 => lecture sur front montant
        MEM=read(MEM,i) # je lis un bit , et je le mets dans la memoire tampon
        fsmup(20) # vingt coups de clock pour la machine d'état
        down() # SPI_CLK passe à zero => mettre la donnée dispo.
        digit=(data>>i)&0x1
        GPIO.output(MOSI,digit)
        fsmup(20) # vingt coups de clock pour la machine d'état
    return MEM


# GPIO.output(CS3, 1) # SSN PULL UP

GPIO.output(RST, 0); GPIO.output(RST, 1)#= RESET

GPIO.output(CS3, 0) # SSN PULL UP
fsmup(20)
envoie_8b(ord('w'))
envoie_8b(0)
envoie_8b(0b00010001)
GPIO.output(CS3, 1)
fsmup(20)

GPIO.output(CS3, 0) # SSN 
fsmup(20)
envoie_8b(ord('r'))
envoie_8b(0)
MEM=envoie_8b(0xff)
GPIO.output(CS3, 1)
fsmup(20)
bin(MEM)


