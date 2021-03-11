
# This experiment is like cp_experiments/shift_register/SR74HC595_experiment3.py
# except that, instead of inheriting from the SR74HC595 class I define a class
# similar to SR74HC59 defined in sr74HC595.py but only uses on_pins to set the pins that are on.

# The other difference is that I have defined a DebouncedLightsButton class that
# uses an IRQ callback on the button with debouncing


import machine
import time
import sr74HC595

# This class keeps track of the number of lights that should be on using an IRQ callback
# and debouncing
class DebouncedLightsButton(machine.Pin):

    # number of retries of the buttons value to determine if the value is stable
    RETRIES = 40
    
    def __init__(self, pinnum, pinupdown, irq):
        super().__init__(pinnum, machine.Pin.IN, pinupdown)
        # setup an IRQ triggered callback for the button
        self.irq(trigger=irq, handler=self.callback)
        self._num_lights = 1
        self.required_value = 0 if irq == machine.Pin.IRQ_FALLING else 1

    def debounce(self):
        # return True iff the button is stable at 1 over RETRIES checks
        curr = self.value()
        if curr != self.required_value:
            return False
        for _ in range(self.RETRIES):
            next_ = self.value()
            if curr != next_:
                return False
            curr = next_
        return True
    
    def callback(self, _):
        # callback for button
        if self.debounce():
            self._num_lights = self._num_lights % 7 + 1
    
    @property
    def num_lights(self):
        return self._num_lights
    
button = DebouncedLightsButton(13, machine.Pin.PULL_DOWN, machine.Pin.IRQ_RISING)

latch_pin =  machine.Pin(6, machine.Pin.OUT)

potentiometer = machine.ADC(machine.Pin(26))

spi = machine.SPI(0, baudrate=5000000, polarity=0, phase=0,
                  sck=machine.Pin(2), mosi=machine.Pin(3),
                  bits=8)

sr = sr74HC595.SR74HC595(spi, latch_pin)

def main():
    
    while True:
        for index in range(8):
            sr.on_pins = (index+offset \
                          for offset in range(button.num_lights))
        
            delay = potentiometer.read_u16()/200000
            time.sleep(delay)
 

if __name__ == "__main__":
    main()