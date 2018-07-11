
import smbus, time
# ls /dev/i2c-1  => smbus(1)
bus=smbus.SMBus(1)
# address check with $>  i2cdetect -y 1
# 10: -- -- -- -- 14 15 16 17 -- -- -- -- -- -- -- 1f 
# 20: -- -- -- -- 24 25 26 27 -- -- -- -- -- 2d -- -- 

gpio1=0x14
gpio2=0x24


bus.write_byte_data(gpio1 ,0xfe, 0xff)

block=bus.read_i2c_block_data(gpio2, 0xff, 2)
print("{:08b} 0x{:02x} | {:08b} 0x{:02x} ".format(block[0],block[0],block[1],block[1]))


