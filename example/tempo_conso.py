import AlimE3631A
alim=AlimE3631A.AlimE3631A("/dev/ttyUSB0")

# from lmk_conf import *
import struct
reg=tableau[12]

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
