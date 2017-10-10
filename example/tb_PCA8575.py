#!/usr/bin/env python
import smbus, time

# ls /dev/i2c-1  => smbus(1)
bus=smbus.SMBus(1)
# AT=0x21
R3=0x23
R8=0x27
# address check with $>  i2cdetect -y 1
# help(bus.read_byte_data)
# help(bus.read_i2c_block_data)

bus.write_byte_data(R3,0xff,0xff) # high logic
bus.write_byte_data(R3,0x00,0x00) # low logic
bus.write_byte_data(R8,0xff,0xff)

bus.write_byte_data(R8,0xa7,0xe7)
bus.read_byte(R8) #=> 167 == 0xa7
bus.read_byte_data(R8,0xff,1)
bus.read_i2c_block_data(R8, 0x0, 1)
#ret=bus.read_byte_data(R8,0) #<== INNUTILISABLE avec gpioExpander NXP
bus.read_i2c_block_data(R8, 0x0, 2) #<== mange des bits ?
#=> [0, 35]#<= au lieu de [0, 231] ?

bus.write_byte_data(R8,0xff,0xff)
bus.read_i2c_block_data(R8, 0xff, 4) #<== mange des bits ?
# maybe not, since it is a floating input, it can be whatever right ?

#bus.read_byte_data(R8,0xff)
print  "0x{:02x}".format(167) #=> 0xa7
print  "0x{:02x}".format(35) #=> 0x23
print  "0x{:02d}".format(0xe7) #=> 231


# /!\ Fck*$$ing driver with the writing cmd
# (in my case the device does not have cmd functionnality, and thus do not expect a write action before a read action.)

# sudo sh -c 'echo N > /sys/module/i2c_bcm2708/parameters/combined'
# sudo sh -c 'echo Y > /sys/module/i2c_bcm2708/parameters/combined'
# does not change anything

bus.write_byte_data(R8,0xff,0xff)
bus.read_i2c_block_data(R8, 0, 1) 

block = bus.read_i2c_block_data(R8, 0, 16) 
print ret

bus.write_byte_data(R3,0xaa,0x5e)
read(R3)

def read(r):
    block = bus.read_i2c_block_data(r, 0, 2)
    print  "{:08b} {:08b} | 0x{:02x}".format(block[0],block[1],block[1])


def readP0(r):
    block = bus.read_i2c_block_data(r, 0, 2)
    print  "{:08b} {:08b} | 0x{:02x}".format(block[0],block[1],block[1])


def readP1(r):
    block = bus.read_i2c_block_data(r, 1, 2)
    print  "{:08b} {:08b} | 0x{:02x}| 0x{:03d}".format(block[0],block[1],block[1],block[1])

readP1(R3) ; readP1(R3)
i=0
bus.write_byte_data(R3,~(i>>1),0x00) ; i=i+1; read(R8)


## i=0
## mask=1<<i
## #mask=~mask
## M1=~mask
## M2=~(mask>>8)
## M3=~(mask>>16)
## M4=~(mask>>32)
## bus.write_byte_data(R1,M1,M2)
## bus.write_byte_data(R2,M3,M4)
## i+=1
## i%= 1<<32
## print i

def closeAll():
    bus.write_byte_data(R1,0xff,0xff)
    bus.write_byte_data(R2,0xff,0xff)
    bus.write_byte_data(R3,0xff,0xff)
    bus.write_byte_data(R4,0xff,0xff)
    bus.write_byte_data(R5,0xff,0xff)
    bus.write_byte_data(R6,0xff,0xff)
    bus.write_byte_data(R7,0xff,0xff)
    bus.write_byte_data(R8,0xff,0xff)

    
off=0xff

# Channel 1 est Y63 puis on tourne dans les aiguilles d'une montre


def shift8 (i, rev=False):
    return ~(1<< (7-(i%8))) & 0xff if rev else ~(1<<(i%8)) & 0xff


def regShift(i,r):
    mask=0xFF
    if  ( i< 1*8 and r==0 ) or (1*8 <= i< 2*8 and r==1) :
        mask=shift8(i, 1)
    return mask

# verification
[regShift(i,0) for i in range(16)]
[regShift(i,1) for i in range(16)]

["{:08b}".format(regShift(i,0)) for i in range(16)]
["{:08b}".format(regShift(i,1)) for i in range(16)]



## shift8(i, 1) # True
## shift8(i, 0) # False

        
def channelSelect (i):
    """
    numerotation arbitraire zero correspond a Y63, puis
    sens des aiguilles d'une montre jusqu'a 127 (X1)
    """
#    assert(0<=i<128, "channel {} does not exist in [0-127]".format(i))
    assert(0<=i<128)
    closeAll() #<== close all relays
    if   i< 1*8 :# bank1
        mask=shift8(i, 1) ; bus.write_byte_data(R1,off,mask)
    elif i< 2*8 :
        mask=shift8(i, 1) ; bus.write_byte_data(R1,mask,off)
    elif i< 3*8 :
        mask=shift8(i, 1) ; bus.write_byte_data(R2,off, mask)
    elif i< 4*8 :
        mask=shift8(i, 1) ; bus.write_byte_data(R2,mask, off)
    elif i< 5*8 :# bank2
        mask=shift8(i, 0) ; bus.write_byte_data(R3,mask,off)
    elif i< 6*8 :
        mask=shift8(i, 1) ; bus.write_byte_data(R3,off,mask)
    elif i< 7*8 :
        mask=shift8(i, 0) ;  bus.write_byte_data(R4,mask,off)
    elif i< 8*8 :
        mask=shift8(i, 0) ;  bus.write_byte_data(R4,off,mask)
    elif i< 9*8 :# bank3
        mask=shift8(i, 0) ; bus.write_byte_data(R6,mask,off)
    elif i< 10*8 :
        mask=shift8(i, 0) ; bus.write_byte_data(R6,off,mask)
    elif i< 11*8 :
        mask=shift8(i, 1) ; bus.write_byte_data(R5,mask,off)
    elif i< 12*8 :
        mask=shift8(i, 1) ; bus.write_byte_data(R5,off,mask)
    elif i< 13*8 :# bank4
        mask=shift8(i, 0) ; bus.write_byte_data(R8,mask,off)
    elif i< 14*8 :
        mask=shift8(i, 0) ; bus.write_byte_data(R8,off,mask)
    elif i< 15*8 :
        mask=shift8(i, 0) ; bus.write_byte_data(R7,off,mask)
    elif i< 16*8 :
        mask=shift8(i, 0) ; bus.write_byte_data(R7,mask,off)
    return mask


# 1 DOIT ALLUMER y1
# 2 DOIT ALLUMER y2 etc.
# ...

def channelSelectY(y):
    if y % 2: # si impaire
        channelSelect((63-y)/2)
    else:
        channelSelect((y/2)+63)


def channelSelectX(x):
    if x % 2: # si impaire
        channelSelect( (65-x)/2 + 95 )
    else:
        channelSelect( (x+62)/2 )







        
if __name__ == '__main__':

    for i in range(1, 65):
        time.sleep(0.4)
        channelSelectX(i)

    for i in range(1, 65):
        time.sleep(0.4)
        channelSelectY(i)

# channelSelectY(1)
        
        
##  chenillard
    i=0 #8*8-1
    for i in range(0, 128) :
        mask=channelSelect(i); 
        print i, i/8, "{:08b}".format(mask)
        time.sleep(0.4)

