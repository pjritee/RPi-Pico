# The other side of data_logger.py
# This requests a download of the logged data from the Pico

import serial
import time

conn = serial.Serial('/dev/ttyUSB0', baudrate = 115200,timeout=1)

# file to save downloaded data
DATAFILE = 'data.csv'
# time/date format to be used for writing time
DATE_TIME_FORMAT = '%d/%m/%y %H:%M:%S'

def parse(line):
    # note that if the data does not parse an exception will be raised
    # that is handled in get_data
    # check that there are 3 comma seperated items
    sample_time, temperature, humidity = line.split(',')
    # check that temperature and humidity are floats
    temperature, humidity = float(temperature), float(humidity)
    # sample_time should be an int
    # I need to use gmtime here to get the right date/time
    time_struct = time.gmtime(int(sample_time))
    # turn the parsed values back to string
    return "{0}, {1}, {2}".format(time.strftime(DATE_TIME_FORMAT, time_struct),
                                temperature, humidity)
    
def get_data():
    # the download has not started yet
    start_download = False
    data = []
    # request a download
    conn.write('get\n'.encode())
    while True:
        try:
            text = conn.readline().decode().strip()
            if not text:
                # a timeout occurred
                if start_download:
                    # we have started a download but we get a timeout - treat
                    # as error
                    conn.write('error\n'.encode())
                    return None
                else:
                    # we haven't started a download yet so keep trying
                    continue
            if text == 'end':
                # the download is complete
                # send acknowledgement
                conn.write('ok\n'.encode())
                return data
            # the download has started
            start_download = True
            # append the parsed text
            data.append(parse(text))
        except Exception as e:
            conn.write('error\n'.encode())
            print('Exception', str(e))
            return None


data = get_data()
if data is None:
    print("failed to download data")
else:
    with open(DATAFILE, 'w') as fd:
        fd.write('\n'.join(data) + '\n')
    print("download successful")
    
