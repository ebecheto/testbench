#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spidev

spi=spidev.SpiDev()
spi.open(0,0)
#spi.max_speed_hz=27000000 #<= 27MHz
#spi.max_speed_hz=10000 #<== 10k
spi.max_speed_hz=100000
#<= 100k # import argparse


def ch2string(ch=1):
    l_bits="0"*(ch-1)+"1"+"0"*(16-ch)
    l_bits=l_bits[:8]+" "+l_bits[8:]
    return l_bits[::-1] #<== reverse string

def codeOne(ch=1):
    """ call this func from 1 to 16"""
    bits=ch2string(ch)
    return map(lambda x: int(x,2)&0xff, bits.split(' '))

def bit2reg(nbShift):
    regs=[0,0,0,0]
    chip=nbShift/8
    regs[chip]=1<<(nbShift-8*chip)
    return regs

def bit4reg(nbShift):
    regs=[0,0,0,0,0,0,0,0]
    reg8=nbShift/8
    regs[reg8]=1<<(nbShift-8*reg8)
    return regs


# for bit in range(64):
#     bit4reg(bit)    

for i in range(64):
    reg2send=bit4reg(i)
#    print "{}".format(reg2send)
    raw_input("Xfert#{:>2}".format(reg2send))
    spi.xfer2(reg2send)


# if loop:
#     for ch in range(1,17):
#         code=map(lambda x: int(x,2), ch2string(ch).split(' '))
#         print "code:", code
#         spi.xfer2(code)
#         raw_input("Xfert#{:>2}, {:>3d} {:>3} == {:08b} {:08b} ".format(ch, code[0],code[1],code[0],code[1]))
# else:
#     for octet in code:
#         print "Xfert code:{}, {:>3} == {:08b} == 0x{:x}".format(code, octet, octet, octet)
#     spi.xfer2(code)

# spi.close()

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
