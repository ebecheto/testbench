#!/usr/bin/env python
# -*- coding: utf-8 -*-

code=[
0x80020140      ,#0	
0x00020800      ,#0	
0x00000041      ,#1	
0x00000802      ,#2	
0x00000803      ,#3	
0x00000804      ,#4	
0x00000085      ,#5	
0x55550006      ,#6	
0x55550007      ,#7	
0x55550008      ,#8	
0x55555549      ,#9	
0xD5C2400A      ,#10	
0x3401102B      ,#11	
0x138C006C      ,#12	
0x3B03826D      ,#13	
0x0400000E      ,#14	
0xC1550410      ,#16	
0x00000018      ,#24	
0xAFA7FE1A      ,#26	
0x0020001C      ,#28	
0x0180021D      ,#29	
0x0100021E      ,#30	
0x001F001F      ,#31
]
row=code[0]
bytearray(struct.pack('<I', row))

pack=list(bytearray(struct.pack('<I', row)))
row #=> 2147615040L
pack=list(bytearray(struct.pack('<I', row)))
spi.xfer2(pack)
#pack a l'air d'être purgé par spi.xfer2
pac=list(bytearray(struct.pack('<I', row)))
spi.xfer2(pac)
spi.xfer2(list(bytearray(struct.pack('<I', row))))
>>> ["{:08b}".format(p) for p in pack]
['01000000', '00000001', '00000010', '10000000']
