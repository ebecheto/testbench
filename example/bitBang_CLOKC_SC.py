#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spidev
import RPi.GPIO as GPIO
import os; from time import sleep
os.system("sudo dtparam spi=on") #<== enable spi
spi=spidev.SpiDev(); spi.open(0,0)
os.system("sudo dtparam spi=off") #<== disable spi => BITBANG possible
# print "pause 2sec wait for modprobe init" # time.sleep(0.1)

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
CS1, CS2, CS3, LMK = 0, 5, 6, 13
MISO, MOSI, SPI_CLK = 9, 10, 11
RST=19; CLOCK_SC = 26 # Choix prendre GPIO26 pour CLOCK_SC_20MHz
CS_LISTE=[CS1, CS2, CS3, LMK, RST, CLOCK_SC, MOSI, SPI_CLK]
[GPIO.setup(CS, GPIO.OUT, initial=0) for CS in CS_LISTE]
GPIO.setup(MISO, GPIO.IN)
# GPIO.cleanup() 

SDN_P3V3=02
SDN_VDD_X=03
SDN_VDD_RO=04
SDN_VDDD_RO=17
SDN_VDD_LC=14
SDN_VDDD_LC=15
SDN_VDD_DRIVER=23#<== remap hardware FIX /!\ 5V

SONDE_LISTE=[SDN_P3V3, SDN_VDD_X, SDN_VDD_RO,SDN_VDDD_RO, SDN_VDD_LC, SDN_VDDD_LC, SDN_VDD_DRIVER]

[GPIO.setup(SONDE, GPIO.OUT, initial=0) for SONDE in SONDE_LISTE]
#[GPIO.output(SONDE, 0)          for SONDE in SONDE_LISTE]
[GPIO.output(SONDE, 1)          for SONDE in SONDE_LISTE]
[GPIO.input(SONDE)          for SONDE in SONDE_LISTE]
# ENABLE OR DISABLE BY SOFTWARE

centu=0.0001 #<= 100us .
GPIO.output(RST, 0); GPIO.output(RST, 1); GPIO.output(RST, 0)#= RESET, fait apres aussi

def writeByte(byte, iM):
    digit=(byte>>iM)&0x1; GPIO.output(MOSI,digit)


MEM=0
def read(MEM, i, bit):
    MEM = MEM | (bit<<i) if bit else MEM & ~(1<<i)&0xff
    return MEM

TAP=-1
spi_clk=0
fsm_clk=0
spi_clk_old= spi_clk
fsm_clk_old= fsm_clk
iM=0 #<= bit d'adressage de la mémoire [0-7]
iW=0 #<= bit d'adressage de Write [0-7]
byte=0
WRITE=0 ; READ=0
delai=0
demiT_spi=500
WRb=200
Word_t=8*2*demiT_spi
T_spi=2*demiT_spi #<== espace entre deux trames : une période de spi_clk
READ_tap=WRb+3*Word_t+T_spi
reg=0x1 #register
data=0xa5
#MAX_TAP=1000000
MAX_TAP=READ_tap+3*Word_t+T_spi+3*T_spi # <= plus 3 trames SPI de marge, temps de FIN

while(TAP<=MAX_TAP):
    TAP+=1; spi_clk_old= spi_clk; fsm_clk_old= fsm_clk

    if(TAP%25==delai):
        fsm_clk = 0 if fsm_clk else 1
        GPIO.output(CLOCK_SC, fsm_clk)

    if(TAP%demiT_spi==0):# %500
        spi_clk = 0 if spi_clk else 1
        GPIO.output(SPI_CLK, spi_clk)

    if(TAP==100):
        GPIO.output(RST, 0); # sleep(centu)

    if(TAP==125):
        GPIO.output(RST, 1); # sleep(centu)

    if(TAP==150):
        GPIO.output(RST, 0); # sleep(centu)#= RESET

    if(TAP==WRb-1):
        GPIO.output(CS3, 0); # sleep(centu)#<== SSN DOWN
        
    if(TAP==WRb):
        WRITE=1; byte=ord('w'); iW=0

    if(TAP==(WRb+Word_t)):
#        raw_input("WRITE== ?{} ?{} ?{}".format(WRITE,spi_clk,  spi_clk_old))
        WRITE=1; byte=reg;      iW=0

    if(TAP==(WRb+2*Word_t)):
        WRITE=1; byte=data;     iW=0

    if(TAP==(WRb+3*Word_t+T_spi/2)):
        WRITE=0; GPIO.output(CS3, 1); # sleep(centu)#<== SSN UP

    if(TAP==READ_tap-1):
        GPIO.output(CS3, 0); # sleep(centu)#<== SSN DOWN

    if(TAP==READ_tap):
        WRITE=1
        byte=ord('r')
        iW=0

    if(TAP==(READ_tap+1*Word_t)):
        WRITE=1
        byte=reg
        iW=0

    if(TAP==(READ_tap+2*Word_t)):
        READ=1
        WRITE=1
        byte=0xff
        iW=0
        iM=0

    if(TAP==READ_tap+3*Word_t+T_spi/2):
       READ=0;       GPIO.output(CS3, 1); # sleep(centu)#<== SSN UP

      
    # nedge
    if(spi_clk==0 and spi_clk_old==1 and WRITE==1 and iW<=7):    # data to put on wire== WRITE 1 bit
        writeByte(byte, 7-iW)#<= MSB FIRST
        print "TAP{}, W{:08b}|{}|{:02x}|[{}].in(SPI_CLK)={}_edge{}old{}".format(TAP,byte,int(byte),byte, iW, GPIO.input(SPI_CLK), spi_clk, spi_clk_old)
        iW+=1

    # rising edge
    if(spi_clk==1 and spi_clk_old==0 and READ==1 and iM<=7):
        # data to put on wire
        bit=GPIO.input(MISO)
        MEM=read(MEM, 7-iM, bit) # je lis un bit , et je le mets dans la memoire tampon MSB FIRST
        print "MEM[{}]=={}#<= !=0 ?".format(iM, MEM)
        iM+=1

#FIN WHILE()

print MEM


