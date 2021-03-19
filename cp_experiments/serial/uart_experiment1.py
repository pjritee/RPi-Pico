# This experiment is similar to am2320_to_serial_experiment.py
# except it does "real" serial communication
# Instead of waiting for a command it simply sends temperature and humidity data every 10 secs
# An Adafruit CP2104 Friend is used for serial communication.
# 
import board
import busio
import time
import adafruit_am2320

# GP12 is UART0 TX  (connected to CP2104 RXD)
# GP13 is UART0 RX  (connected to CP2104 TXD)
# CP2104 GND is connected to GROUND
# CP2104 3V is connected to 3V power

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