# Modification of ShiftRegister74HC595_experiment2.py
# In that version I needed to do bit fiddling
# at the top-level
# In this example I define a subclass of
# ShiftRegister74HC595
# and hide the bit fiddling in there
#
# If you are reading this and are not very familiar
# with Python - this is a reasonably advanced idea.
#
# It uses subclassing and property decorator

# For a tutorial on subclassing and super perhaps try
# something like:
# https://realpython.com/python-super/
# For getters/setters and properties perhaps try:
# https://www.python-course.eu/python3_properties.php

# To test try the following in the REPL
# (make sure you save this file on the Pico)

# from ShiftRegister74HC595_experiment3 import *
# sr.on_pins = [1,3]

# this should turn on pins 1 and 3 (only)

# sr.on_pins

# should display [1,3]

import board
import digitalio
import adafruit_74hc595
import busio
import time
import analogio

# Subclass of ShiftRegister74HC595
class ExtendedShiftRegister74HC595(adafruit_74hc595.ShiftRegister74HC595):
 
    def __init__(self, spi,  latch):
        super().__init__(spi,  latch)
        # initialize gpio (all pins unset)
        self.gpio = 0
        
    @property
    def on_pins(self):
        pins = self.gpio
        # Return the list of pin numbers whose
        # corresponding bit in gpio is 1
        return [p for p in range(8) if pins & (1 << p)]
    
    @on_pins.setter
    def on_pins(self, onpins):
        pins = 0
        # set the bits corresponding to pin numbers
        # note pin numbers taken mod 8 to restrict the
        # pin numbers to 0..7
        # this means, for example on_pins = [-1]
        # will set pin 7
        for p in onpins:
            pins |= 1 << (p % 8)
        if pins != self.gpio:
            # only update gpio if at least one bit has changed
            self.gpio = pins
            
button = digitalio.DigitalInOut(board.GP13)
button.switch_to_input(pull=digitalio.Pull.DOWN)

latch_pin =  digitalio.DigitalInOut(board.GP6)
latch_pin.direction = digitalio.Direction.OUTPUT

potentiometer = analogio.AnalogIn(board.GP26)
   
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3)

spi.try_lock()
spi.configure(baudrate=5000000, phase=0, polarity=0)
spi.unlock()

# Use the subclass defined above
sr = ExtendedShiftRegister74HC595(spi, latch_pin)

def main():
    num_lights = 1
    button_pressed = False
    
    while True:
        for index in range(8):
            # update number of lights if button is pressed
            if button.value and not button_pressed:
                button_pressed = True
                num_lights = num_lights % 7 + 1
            if not button.value and button_pressed:
                button_pressed = False
    
            # now this bit is simple (relatively speaking)
            # note I have used a generator and not a list
            # but that's OK as the class can cope with
            # any iteration of ints
            sr.on_pins = (index+offset \
                          for offset in range(num_lights))
        
            delay = potentiometer.value/200000
            time.sleep(delay)
 
# If you haven't seen the code below this is the standard way
# of giving the choice of running the code (eg by pressing
# the run button) and importing the code (as suggested above)
# so you can test or experiment without getting stuck
# in the infinite loop
if __name__ == "__main__":
    main()