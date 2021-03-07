# Using the SerialAm2320 class in serial_am2320.py to access the data on the
# am2320. This is very simple but the idea would be to produce an app that
# uses this interface to monitor temp/humidity.
# Alternatively, it could be used as part of a "weather web server"

import serial_am2320
import time

# create an object
weather = serial_am2320.SerialAm2320('/dev/ttyACM0')


while True:
    print(weather.data)
    time.sleep(5)
