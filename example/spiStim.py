#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spidev

spi=spidev.SpiDev()
spi.open(0,0)
#spi.max_speed_hz=27000000 #<= 27MHz
# spi.max_speed_hz=10000 #<== 10k
spi.max_speed_hz=100000 #<= 100k
#spi.mode=0b11
#spi.max_speed_hz=1000000 #<= 1M
# spi.lsbfirst = False
# ligne=[int(code, 16)>>8, int(code, 16)&0xff]
# spi.writebytes([(1<<(ch-1))&0xFF])
# spi.xfer2([(1<<(ch-1))>>8&0xFF,(1<<(ch-1))&0xFF])

import argparse
parser = argparse.ArgumentParser(description='send spi bits')
parser.add_argument('-bits', default="01010101 01010101", help='octet strings to send')
parser.add_argument('-rst', action='store_true', default=False, help='force reset')
parser.add_argument('-on', action='store_true', default=False, help='force all ON')
parser.add_argument('-loop', action='store_true', default=False, help='loop/pause')
parser.add_argument('-ch', type=int, default=0, help='active only 1 channel')
parser.add_argument('-out', type=int, default=0, help='ch 1 == out<0>')
args = parser.parse_args();
ch=args.ch if not(args.out) else args.out+1
loop=args.loop
l_bits=args.bits
# chan "12345678 9ABCDEFG"
l_bits="00000000 00000000" if args.rst else l_bits
l_bits="11111111 11111111" if args.on  else l_bits

def ch2string(ch=1):
    l_bits="0"*(ch-1)+"1"+"0"*(16-ch)
    l_bits=l_bits[:8]+" "+l_bits[8:]
    return l_bits

if ch:
    l_bits=ch2string(ch)
#    print l_bits, ch

print args.bits, args.rst, args.on, args.ch
l_bit=l_bits.split(' ')

#____12345678
# ena="01010101"
# rst="00000000"
# all="11111111"
#bits="10000000"
code=map(lambda x: int(x,2), l_bit)
# code string transfered, from base 2, into integer
# code=int(bits, 2)
print code
# spi.xfer2([0,0])


if loop:
    for ch in range(1,17):
        code=map(lambda x: int(x,2), ch2string(ch).split(' '))
        print "code:", code
        spi.xfer2(code)
        raw_input("Transfert, {} {} == {:08b} {:08b} ".format(code[0],code[1],code[0],code[1]))
else:
    for octet in code:
        print "Transfert, {} == {:08b} == 0x{:x}".format(octet, octet, octet)
    spi.xfer2(code)

spi.close()

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
