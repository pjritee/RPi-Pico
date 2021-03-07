# The Pico side of the serial connection for
# accessing an am2320 temperature/humidity sensor
#
# When this side reads the string ';;get_temp;;'
# it responds by using I2C comms to access the am2320
# and sends the data over the serial line.
#
# Note the comments in the README about this sort of serial
# communication

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
    if cmd == ';;get_temp;;':
        print('data({{"temperature":{0}, "relative_humidity":{1}}})'.\
              format(sensor.temperature, 
                     sensor.relative_humidity))
