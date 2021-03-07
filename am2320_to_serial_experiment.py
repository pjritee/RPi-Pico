import board
import digitalio

import busio
import adafruit_am2320

# using I2C for temp/hum sensor
i2c = busio.I2C(board.GP9, board.GP8)
# the sensor is an AM2315 (the am2320 lib works)
sensor = adafruit_am2320.AM2320(i2c)

while True:
    cmd = input().strip()
    print(cmd)
    if cmd == 'get':
        print('data({{temperature:{0}, relative_humidity:{1}}})'.\
              format(sensor.temperature, 
                     sensor.relative_humidity))
    else:
        break