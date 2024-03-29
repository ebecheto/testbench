#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0
# ,Data[26 :0],,,,,,,,,,,,,,,,,,,,,,,,,,,Address[4:0],,,,
# register,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,4,3,2,1,0
#,31 is missing, replaced by caracter # for commeting
#30292827262524232221201918171615141312111009080706050403020100
import numpy as np

tab=[                                                             #    write cycle	note                                                    
0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  #R0  1	reset                                                          
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,  #R0  2	Out 0 and 1 divider = 64                                       
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,  #R0  3	must be programme twice if >25                                 
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,  #R1  4	Out 2 and 3 divider = 2                                        
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,  #R2  5	Out 4 and 5 divider = 64                                       
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,  #R2  6	must be programme twice if >25                                 
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,  #R3  7	Out 6 and 7 divider = 64                                       
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,  #R3  8	must be programme twice if >25                                 
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,  #R4  9	Out 8 and 9 divider = 64                                       
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,  #R4  10	must be programme twice if >25                                 
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,  #R5  11	Out 10 and 11 divider = 4
0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,  #R6  12	set output mode = LVPECL 2Vpp (for out 3 to 0)                 
0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,  #R7  13	set output mode = LVPECL 2Vpp (for out 7 to 4)                 
0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,  #R8  14	set output mode = LVPECL 2Vpp (for out 11 to 8)                
0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,1,  #R9  15	« program as shown for proper operation »                      
0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,  #R10 16	disable OSCout1, enable OSCout1, set LVPECL 2Vpp               
0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,  #R11 17	configure sync and xtal (external XO)                          
0,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,  #R12 18	LD_MUX=2 (PLL DLD) ; LD_TYPE=3 (output, logic high)            
0,0,1,1,1,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,  #R13 19	readback_type=0x03(output, pushpull) ; GPout0=0                
0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,  #R14 20	GPout1=3.3V                                                    
1,1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,  #R16 21	« program as shown for proper operation »                      
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,  #R24 22	C4,C3,R4,R3 (0x00)                                             
1,0,1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,1,0,  #R26 23	en_pll_ref_2x=0 ; pll_cp_gain=3.2mA(0x03);pll_dld_cnt=16(0x100)
0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,  #R28 24	PLL_R=1 (0x2)
0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,1,  #R29 25	OSCin_FREQ=80MHz(0x01) ; PLL_N_CAL=16
0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,0,  #R30 26	PLL_P=2 ; PLL_N=16
0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,  #R31 27	READBACK_ADDR=3, uWire_LOCK=0                                  
]
tableau=np.split(np.array(tab), 27)


# np.array(["0b"+"".join([str(i) for i in reg]) for reg in tableau]) #<= view
