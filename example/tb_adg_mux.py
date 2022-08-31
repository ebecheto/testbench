import spidev

spi=spidev.SpiDev(); spi.open(0,0)
spi.max_speed_hz=500000 #<= 500k
spi.mode=0b10 #<== mode 2 : CS Down, data clocked on falling edge

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
CSU1, CSU2= 29, 31
[GPIO.setup(CS, GPIO.OUT) for CS in CSU1, CSU2]
[GPIO.output(CS, 1) for CS in CSU1, CSU2]

def send(i,CS):
    GPIO.output(CS,0)
    spi.xfer2([i])
    GPIO.output(CS,1)

send(0,CSU1)
send(0xFF,CSU1) # for some reason i have to reset the vable besore selecting another one.
send(1,CSU1)

for i in range(16):
    send(0xFF,CSU1)
    send(i,CSU1)
    raw_input("i={}".format(i))

for i in range(16):
    send(0xFF,CSU2)
    send(i,CSU2)
    raw_input("i={}".format(i))



# spi.xfer2([0]) #<== pin number 1 ON 
# spi.xfer2([31])#<== enable last MUX : 32
# spi.xfer2([0xFF])

# for i in range(32):
#     null=spi.xfer2([i])
#     null=raw_input("[{}]next:1".format(i))
