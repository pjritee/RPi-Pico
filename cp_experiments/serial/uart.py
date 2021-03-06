import board
import busio
import time
import adafruit_am2320

uart = busio.UART(board.GP12, board.GP13, baudrate=115200)

# using I2C for sensor
i2c = busio.I2C(board.GP9, board.GP8)
# the sensor is an AM2315
sensor = adafruit_am2320.AM2320(i2c)

# Write data in json format to serial every 10 secs
while True:
    data = '{{"temperature":{0}, "relative_humidity":{1}}}\n'.\
              format(sensor.temperature, 
                     sensor.relative_humidity)
    uart.write(data.encode())
    time.sleep(10)