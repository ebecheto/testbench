
#!/usr/bin/env python
import smbus, time

# ls /dev/i2c-1  => smbus(1)
bus=smbus.SMBus(1)
AT=0x27
# address check with $>  i2cdetect -y 1

filename="register.txt"
with open(filename, 'r') as f:
  ioss=int(f.next())

ios=ioss if 0<=ioss<=65535 else 0


bus.write_byte_data(AT,0xff,0xff)
bus.write_byte_data(AT,0x00,0x00)

# GPIO EXPANDER pinout : 
# ON_1 : P00  P10 : OFF_1
# ON_2 : P01  P11 : OFF_2
# ON_3 : P02  P12 : OFF_3
# ON_4 : P03  P13 : OFF_4
# ON_5 : P04  P14 : OFF_5
# ON_6 : P05  P15 : OFF_6
# ON_7 : P06  P16 : OFF_7
# ON_8 : P07  P17 : OFF_8

# Demarrage : Rpi (USB meter) = 500mA
bus.write_byte_data(AT,0x00,0xff)# 670 mA 'clic' des 4 relais
bus.write_byte_data(AT,0xff,0xff)# => 500mA => plus de conso des relai
# commutation sans bruit

bus.write_byte_data(AT,0xff,0x00)# 750mA 'clac' des 4 relais
bus.write_byte_data(AT,0xff,0xff)# 500mA => pause plus de conso normallement
# commutation sans bruit

port0=0xff
port1=0xff
ios=(port1<<8)|(port0&0xff)

print "P0 {0:02x} : {1:08b}".format(port0,port0)
print "P1 {0:02x} : {1:08b}".format(port1,port1)
print "register {0:04x} : {1:16b} {2:d}".format(ios,ios,ios)

  

FILE = open(filename,"w")
FILE.write("{}".format(ios))
FILE.close()



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

