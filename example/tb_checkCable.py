#!/usr/bin/env python
# -*- coding: latin-1 -*
import smbus, time
import numpy as np
from math import floor
# ls /dev/i2c-1  => smbus(1)
bus=smbus.SMBus(1)
# address check with $>  i2cdetect -y 1
# 10: -- -- -- -- 14 15 16 17 -- -- -- -- -- -- -- 1f 
# 20: -- -- -- -- 24 25 26 27 -- -- -- -- -- 2d -- -- 

TOP=[0x14, 0x15, 0x16, 0x17, 0x1f]
BOT=[0x24, 0x25, 0x26, 0x27, 0x2d]


def read2bxd(r):
    block = bus.read_byte(r)
    print  "{:08b} | 0x{:02x} | {}".format(block,block,block)

def read(r):
    block = bus.read_i2c_block_data(r, 0xff, 2)
#    print("{:08b} 0x{:02x} | {:08b} 0x{:02x} ".format(block[0],block[0],block[1],block[1]))
    return block
    

def shift8 (i, rev=False):
    return ~(1<< (7-(i%8))) & 0xff if rev else ~(1<<(i%8)) & 0xff

def setOne(i, rev=False):
    P0=0xff;P1=0xff
    if  ( i< 1*8 ):
        P0=shift8(i, rev)
    elif (1*8 <= i< 2*8 ) :
        P1=shift8(i, rev)
    return [P0,P1] #<= return MSB first ? NO just fot printing latter
# setOne(1)[0]
#     setOne(1)[1]

def number2tik(num, tik='-',rev=-1):
    """Useful for pretty print read byte rev==-1 for reverse order"""
    return ''.join(['x' if x=='0' else tik for x in list("{:08b}".format(num))[::rev] ])


def number2tikx(num, tik='-'):
    """Useful for pretty print read byte """
    return ''.join(["{:1x}".format(num) if x=='0' else tik for x in list("{:08b}".format(num)) ])


#[number2tikx(i) for i in range(16)]

def number2x(num, tik='-'):
    """Useful for viewing/checking writing pattern. 
       Read does not have to be reversed! """
    return ''.join(['x' if x=='0' else tik for x in list("{:08b}".format(num)) ][::-1]) #<== [::-1] for reverse printing => zero on left etc.

def number2x_check():
    for i in range(2**8):
        print("{:3}:".format(i)+number2x(i)+"_"),
        if (i+1)%8==0 :
            print("_")

# number2x_check()



def shift8_check():
    ret=["{:08b}".format(shift8(i)) for i in range(8)]
    print "\n".join(ret)

# shift8_check()

def shift2out(i):
    return [(1<<i)&0xFF,((1<<i)>>8)&0xFF ]

# def shift2out_check():
#     ret=["{:08b} {:08b}".format(shift2out(i)[0],shift2out(i)[1]) for i in range(16)]
#     print "\n".join(ret)

# shift2out_check()
# Wrong, take setOne function

def write(reg,i):
    return bus.write_byte_data(reg ,setOne(i)[0],setOne(i)[1])

[bus.write_byte_data(reg ,0x00,0x00) for reg in TOP]#=> outputs==0
[bus.write_byte_data(reg ,0xff,0xff) for reg in BOT]#=> inputs to be read

def pin2write(pin,verb=False):
    ret=[]
    for nb,chip in enumerate(TOP):
        trunk=pin/16#<== integer division => natural floor
        # if nb==trunk :
        #     ret=pin>>(8*nb)
        config=pin-16*nb if nb==trunk else 0xff
        ret.append(config)
        if verb:
            print("{} {:08b}{:08b}".format(chip, setOne(config,1)[0], setOne(config,1)[1]))
        write(chip, config)
    return ret

#pin2write(15)

chip=TOP[0]
write(chip,9)
rr=read(BOT[0])# => [127, 255]
"{:08b} {:08b}".format(rr[0],rr[1])

#=> '01111111'

def readWrite(num,t,b):
    write(TOP[t],num)
    rr=read(BOT[b])# => [127, 255]
    return "".join(map(number2tik, rr))

# readWrite(1,0,0)

def pin2read():
    rd=[]
    for nb,chip in enumerate(BOT):
        rd.extend(read(chip))
    return rd

def prettyPrint(rpins):
    print "".join(map(number2tik, rpins))

def checkCable(Nmax):
    ret=[]
    for i in range(Nmax):
        confs=pin2write(i)
        rpins=pin2read()
        ret.append(rpins)
        print("{:02d}|{:02d}|".format(i+1,Nmax-i)),
        prettyPrint(rpins)
    return ret


#res=checkCable() #=> test 80-pins
res=checkCable(40)

npres=np.array(res)
#np.savetxt('hex_4R.txt', npres, fmt='%.3d')
np.savetxt('hex_4L.txt', npres, fmt='%.3d')
np.savetxt('hex_2L.txt', npres, fmt='%.3d')
np.savetxt('hex_2R.txt', npres, fmt='%.3d')



# # if __name__ == '__main__':
# i=
# res[i][j]
# for i in range(40):
#     prettyPrint(res[i])
# for i in range(40):
#     for j in range(5):
#         print("{:08b}, ".format(res[i][j])),
#     print("")
# with open('hex_4L.txt', 'w') as f:
#     for item in res:
#         f.write("%s\n" % item)
