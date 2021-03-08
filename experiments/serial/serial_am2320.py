# A simple class to interface with an am2320 temperature/humidity sensor
# over a serial connection

# The Pico code responds to reading the string "";;get_temp;;"
# by sending back a string like
# 'data({"temperature": 25.6, "relative_humidity": 86.5})'

import serial
import re
import json
import time

# regular expression for getting the data string
data_re = re.compile(r'data\(([^)]*)\)')

class SerialAm2320(object):
    def __init__(self, port):
        # initialize the serial connection
        self._connection = serial.Serial(port, baudrate = 115200,timeout=1)
        

    @property
    def data(self):
        # ask for the data
        self._connection.write((";;get_temp;;\r\n").encode())
        # give the Pico time to respond
        time.sleep(0.2)
        # get the number of bytes received
        num = self._connection.in_waiting
        if num:
            # something has been received so read it
            data = self._connection.read(num).decode().strip()
            # search the string read in for the data
            match = data_re.search(data)
            if match is None:
                # no match found
                return None
            # match found - extract data and read as a json string
            # producing a dictionary like
            # {"temperature": 25.6, "relative_humidity": 86.5}
            return json.loads(match.group(1))
        else:
            # no data waiting
            return None
