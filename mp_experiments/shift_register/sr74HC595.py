# The MIT License (MIT)
# 
# Copyright (c) 2018 Kattni Rembor for Adafruit Industries
# Copyright (c) 2021 Peter Robinson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This class is inspired by https://github.com/adafruit/Adafruit_CircuitPython_74HC595
# and so the above copyright notice is included.


import machine
import time


class SR74HC595(object):
 
    def __init__(self, spi, latch):
        # initialize pins - all pins unset
        self.pins = bytearray(1)
        self.pins[0] = 0x00
        self.spi = spi
        self.latch = latch
        self.latch.on()
        self.on_pins = []
        
    @property
    def on_pins(self):
        pins = self.pins[0]
        # Return the list of pin numbers whose
        # corresponding bit in pins is 1
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
        # pins &= 0xFF - the above guarantees this?
        if pins != self.pins[0]:
            # pins have changed - write it
            self.pins[0] = pins
            self.latch.off()
            self.spi.write(self.pins)
            self.latch.on()
