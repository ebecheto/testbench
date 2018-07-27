#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smbus, time, spidev

        # """
        # #item= PORT:[0-1], POSITION:[0-7], VALUE:bit
        # """


class MPTDC:
    """# address check with $>  i2cdetect -y 1
    # init gpioExpander
    """
    LOCAL_VAR = 1024
    
    def __init__(self, AT=0x27):
        self.port=0&0xff
        self.AT=AT
        self.spi=spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=10000
        self.bus=smbus.SMBus(1)
        self.bus.write_byte_data(self.AT ,0x6, 0x00)
        self.bus.write_byte_data(self.AT ,0x7, 0x00)
        self.OE0_F=1   # D1
        self.OE1_F=1   # D2
        self.OE2_F=1   # D3
        self.OE3_F=1   # D4
        self.OE4_F=0   # D5
        self.RO_STAY=1 # D6
        self.WBR    =0 # D7
        self.OE0_S  =0 # D8
        self.OE1_S  =0 # D9
        self.OE2_S	=0# D10
        self.OE3_S 	=0# D11
        self.OE4_S	=0# D12
        self.RST    =1# D13
        self.RESULT=0
        self.setBits()
        self.setPort()
    
    def setBits(self):
        self.i2cBits=[
            [0, 0, self.OE0_F  ],
            [0, 1, self.OE1_F  ],
            [0, 2, self.OE2_F  ],
            [0, 3, self.OE3_F  ],
            [0, 4, self.OE4_F  ],
            [0, 5, self.RO_STAY],
            [0, 6, self.WBR    ],
            [0, 7, self.OE0_S  ],
            [1, 0, self.OE1_S  ],
            [1, 1, self.OE2_S  ],
            [1, 2, self.OE3_S  ],
            [1, 3, self.OE4_S  ],
            [1, 4, self.RST    ]
        ]
        return self.i2cBits
    
    def setPort(self):
        """ update i2cBits into binary value 'self.port' """
        port=0
        for item in self.i2cBits:
            port=port| (item[2]<<(item[1]+8*item[0]))
        self.port=port
        return port
    
    def pp(self):
        """ pretty Print ports """
        port=self.port
        print("{:016b}, cad : P1=[{:08b}], P0=[{:08b}]".format(port,port>>8,port&0xff))
        msg=""
        for i, val in enumerate(['OE0_F','OE1_F','OE2_F','OE3_F','OE4_F','RO_STAY','WBR','OE0_S','OE1_S','OE2_S','OE3_S','OE4_S','RST']):
            msg=msg+"[{:7s}: {}]\n".format(val, (port>>i)&0x1)
        print(msg)
    
    def setROF(self, bit, value):
        try:
            bit>5
        except ValueError:
            print("RO bit entre 0 et 4")
        self.i2cBits[bit][2]=value
        self.setPort()
        return self.i2cBits
    
    def setROS(self, bit, value):
        try:
            bit>5
        except ValueError:
            print("RO bit entre 0 et 4")
        self.i2cBits[bit+7][2]=value
        self.setPort()
        return self.i2cBits
    
    def stay(self, val):
        self.RO_STAY=val
        self.setBits()
        self.setPort()
    
    def reset(self, tps=0.1):
        self.RST=0
        self.setBits()
        self.send()
        time.sleep(tps)
        self.RST=1
        self.setBits()
        self.send()
    
    def send(self):
        self.setPort()
        P1=self.port>>8; P0=self.port&0xff
        self.bus.write_byte_data(self.AT ,0x2, P0 &0xff)
        self.bus.write_byte_data(self.AT ,0x3, P1 &0xff)
    
    def setWBR(self, val):
        self.WBR=val
        self.setBits()
        self.send()
    
    def read(self):
        self.setWBR(1)
        self.RESULT=self.spi.xfer2([0]*112)
        self.setWBR(0)
        print("** RES="+str(self.RESULT)+" **")
        return self.RESULT 
    
    def setSlow(self, nb):
        """nb va de 0 à 30 : 31 => pas de courant"""
        for i in range(5):
            bit=i; value=nb>>i&0x1
            self.setROS(bit, value)
    
    def setFast(self, nb):
        """nb va de 0 à 30 : 31 => pas de courant"""
        for i in range(5):
            bit=i; value=nb>>i&0x1
            self.setROF(bit, value)
    
    def stop(self):
        self.stay(0)# STOP
        self.send()
    
    def start(self):
        self.stay(1)# STOP
        self.send()




# tdc=MPTDC()
# tdc.OE0_F=1
# tdc.setBits()
# tdc.setROS(0,1)
# tdc.pp()
# tdc.send()
# tdc.read()

# tdc.setWBR(0)
# tdc.RST=0
# tdc.setBits()
# tdc.ppPort()
# tdc.send()

# tdc.RO_STAY=0
# tdc.setBits()
# tdc.setPort()
# tdc.ppPort()
# tdc.send()

# tdc.RST=1
# tdc.setBits()
# tdc.setPort()
# tdc.ppPort()
# tdc.send()

# tdc.RO_STAY=1
# tdc.setBits()
# tdc.setPort()
# tdc.ppPort()
# tdc.send()

#set LSB=100ps








        # i2cBits=MPTDC().i2cBits
        #setattr( tdc, 'OE0_F', 1 )
# getattr( tdc, 'RST' )
# getattr( tdc, 'i2cBits' )

# def setPort(port,liste):
#     for item in liste:
#         port=port| (item[2]<<(item[1]+8*item[0]))
#     return port


# def setROF(bit, value, i2cBits):
#     try:
#         bit>5
#     except ValueError:
#         print("RO bit entre 0 et 4")
#     print "warning AA" if bit>5 else True
#     i2cBits[bit][2]=value
#     return i2cBits

# def setROS(bit, value, i2cBits):
#     try:
#         bit>5
#     except ValueError:
#         print("RO bit entre 0 et 4")
#     print "warning AA" if bit>5 else True
#     i2cBits[bit+7][2]=value
#     return i2cBits

# port=0
# i2cBits=setROS(0, 0, i2cBits)
# port=setPort(port, i2cBits)
# print("{:016b}, cad : P1=[{:08b}], P0=[{:08b}]".format(port,port>>8,port&0xff))
# P1=port>>8; P0=port&0xff

# #            [0-4], Value, i2cBits

# # i2cBits=setROS(0, 0, i2cBits)
# # i2cBits=setROF(0, 0, i2cBits)
# # port=setPort(0, i2cBits)
# # P1=port>>8; P0=port&0xff
# # bus.write_byte_data(AT ,0x2, P0 &0xff)
# # bus.write_byte_data(AT ,0x3, P1 &0xff)


#     # """slow = [bit,val]
#     #    fast = [bit,val]"""

# def setFrequency(slow, fast, reg=i2cBits):
#     reg=setROS(slow[0], slow[1], reg)
#     reg=setROF(fast[0], fast[1], reg)
#     port=setPort(0, reg)
#     P1=port>>8; P0=port&0xff
#     bus.write_byte_data(AT ,0x2, P0 &0xff)
#     bus.write_byte_data(AT ,0x3, P1 &0xff)

# # setFrequency( [0,0],[0,0])

# for i in range(5):
    
#     for val in range(2):
#         bus.write_byte_data(AT ,0x2, 0b00001100 &0xff)
#         bus.write_byte_data(AT ,0x3, 0b00000110 &0xff)
#         setFrequency( [i, val],[0,0])
#         #readScope
#         raw_input("youhou {}{}".format(i, val))
        






# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# #spi.max_speed_hz=27000000 #<= 27MHz
# #spi.max_speed_hz=10000 #<== 10k
# spi.max_speed_hz=100000
# #<= 100k # import argparse
# # RESULT=spi.xfer2([0]*112)

# #test
# for i in range(5):
#     for val in range(2):
#         bus.write_byte_data(AT ,0x2, 0b00001100 &0xff)
#         bus.write_byte_data(AT ,0x3, 0b00000110 &0xff)
#         setFrequency( [i, val],[0,0])
#         #readScope
#         raw_input("youhou {}{}".format(i, val))

        
