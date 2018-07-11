import bistable
import smbus, time; from time import sleep
import numpy as np

import RPi.GPIO as GPIO ; GPIO.setmode(GPIO.BOARD)
[GPIO.setup(i, GPIO.IN) for i in [31,33,35,37]]
def read(i):
  return GPIO.input(37-2*i)

bi=bistable.bistable(0x27)
bi.AT, bi.reg

bi.addreg(1)
bi.send(1)

bi.regs()


# # Scurve :
# for delay in np.arange(0,0.1,0.001) :
#     k=0
#     for i in range(100):
#         bi.send(1)
#         sleep(delay)
# #        bi.regs()
#         R=bi.read(1)
#         bi.release()
#         bi.send(0)
#         sleep(0.2)
#         k=k+1 if R else k
#     print "delay ; {} ; {}".format(delay, k)
# # delay ; 0.0 ; 0
# # delay ; 0.001 ; 0
# # delay ; 0.002 ; 0
# # delay ; 0.003 ; 0
# # delay ; 0.004 ; 100
# # delay ; 0.005 ; 100
# # delay ; 0.006 ; 100
# # delay ; 0.007 ; 100
# # delay ; 0.008 ; 100
