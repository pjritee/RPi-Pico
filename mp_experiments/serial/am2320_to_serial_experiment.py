

from machine import I2C, Pin
import am2320

i2c = I2C(0, sda=Pin(8), scl=Pin(9))

am = am2320.AM2320(i2c)

while True:
     cmd = input().strip()
     if cmd == ';;get_temp;;':
         am.measure()
         print('data({{"temperature":{0}, "relative_humidity":{1}}})'.\
               format(sensor.temperature(), sensor.relative_humidity()))
