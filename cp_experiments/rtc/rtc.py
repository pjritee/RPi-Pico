# An experiment using the DS3231 RTC (real time clock)
# Following:
# https://learn.adafruit.com/adafruit-ds3231-precision-rtc-breakout/circuitpython

# In order to run this you need to copy adafruit_ds3231.mpy and the adafruit_register directory
# from the adafruit library repository to the lib directory on the Pico

# set up I2C using GP14 (I2C1SDA) and GP15 (I2C1SCL)
# with RTC pins:
#  Vin - pico 3v3 (power)
#  GND - pico GND
#  SCL - pico GP15
#  SDA - pico GP14 


import adafruit_ds3231
import board
import busio
import time

# create an I2C object
i2c = busio.I2C(board.GP15, board.GP14)

# create a DS3231 object
ds3231 = adafruit_ds3231.DS3231(i2c)

#print out the time on the RTC as a time data structure
print(ds3231.datetime)

# the first time you do this (and/or because your battery is flat like mine was) you will
# get a "default time"
# A simple way to initialize the time on the RTC with close to the real time is to run this program
# and then, in the REPL, enter
# ds3231.datetime =
# in preparation to copy a time structure to the RHS followed by pressing RETURN
#
# On your PC start python3 and then do
# >>> import time
# >>> time.localtime()
# and you should get something like
# struct_time(tm_year=2021, tm_mon=3, tm_mday=13, tm_hour=7, tm_min=54, tm_sec=23, tm_wday=5, tm_yday=-1, tm_isdst=-1)
# copy that to the REPL to get
# ds3231.datetime = struct_time(tm_year=2021, tm_mon=3, tm_mday=13, tm_hour=7, tm_min=54, tm_sec=23, tm_wday=5, tm_yday=-1, tm_isdst=-1)
# and now press RETURN
# Hopefully you will only be a few seconds out.
# Now if you unplug/plug the Pico and run the program the correct time should now be printed
# (assuming your battery has charge)

