# This experiment writes to a file on the Pico and so the Pico file systems needs to be writable.
# The instruction in
# https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/data-logger
# did the trick.
# The example on that site does temperature data logging as well but in this experiment I wanted
# to combine data gathering with an RTC and serial communication.

import board
import busio
import time
import adafruit_am2320
import digitalio
import adafruit_ds3231


# GP12 is UART0 TX  (connected to CP2104 RXD)
# GP13 is UART0 RX  (connected to CP2104 TXD)
# CP2104 GND is connected to GROUND
# CP2104 3V is connected to 3V power

uart = busio.UART(board.GP12, board.GP13, baudrate=115200,timeout=2)

# I decided to use 2 I2C's - one for the sensor and one for the RTC.
# 
sensor_i2c = busio.I2C(board.GP9, board.GP8)
# the sensor is an AM2315
sensor = adafruit_am2320.AM2320(sensor_i2c)

rtc_i2c = busio.I2C(board.GP15, board.GP14)
# create a DS3231 object
ds3231 = adafruit_ds3231.DS3231(rtc_i2c)

# LED to turn on when uploading data
upload_led = digitalio.DigitalInOut(board.GP19)
# LED to turn on when in sampling mode (a flash off when taking sample)
sampling_led = digitalio.DigitalInOut(board.GP20)
upload_led.direction = digitalio.Direction.OUTPUT
sampling_led.direction = digitalio.Direction.OUTPUT

DATAFILE = '/data.txt' # file to store data on Pico
SAMPLE_INTERVAL = 10 #secs - how often sample to be taken
SLEEP_TIME = 2 #secs - how long to sleep before testing if an upload is requested
BLOCK_TIME = 6 #secs - for avoiding a "race condition" where an upload/delete is happening
                # when a sample should be taken

# get the time from the RTC as the secs since EPOCH
current_time = time.mktime(ds3231.datetime)

# next_sample is the time at which the next sample is to be taken
# "round it" to the sampling interval so we get nice times
next_sample = SAMPLE_INTERVAL + current_time - current_time % SAMPLE_INTERVAL

# upload the data on the serial line
def upload():
    # flip the LEDs
    upload_led.value = True
    sampling_led.value = False
    # write the data to serial
    with open(DATAFILE, 'r') as fd:
        for line in fd:
            uart.write(line.encode())
    # send a "terminator"
    uart.write("end\n".encode())
    # read a reply 
    reply = uart.readline()
    if reply and reply.decode().strip() == 'ok':
        # the upload succeeded
        # delete file
        with open(DATAFILE, 'w') as fd:
            pass
    else:
        # upload failed for some reason - flash the upload LED
        for _ in range(20):
            upload_led.value = not upload_led.value
            time.sleep(0.2)
    # flip the LEDs back
    sampling_led.value = True
    upload_led.value = False

# delay_upload is True iff a download was requested when a sample is about to be taken
delay_upload = False
while True:
    sampling_led.value = True
    time.sleep(SLEEP_TIME)
    if delay_upload:
        # a sample was just taken and a download was requested
        upload()
        delay_upload = False
    elif uart.in_waiting:
        # something waiting to be read
        cmd = uart.readline().decode().strip()
        if cmd == 'get':
            # a download request
            if abs(next_sample - time.mktime(ds3231.datetime)) < BLOCK_TIME:
                # too close to sample time - delay
                delay_upload = True
            else:
                # ok to upload
                upload()

    if abs(next_sample - time.mktime(ds3231.datetime)) < SLEEP_TIME:
        # close enough to sample time
        sampling_led.value = False
        # append data to file
        fd = open(DATAFILE, 'a')
        fd.write(f"{next_sample},{sensor.temperature},{sensor.relative_humidity}\n")
        fd.close()
        # the next sampling time
        next_sample += SAMPLE_INTERVAL
        sampling_led.value = True
