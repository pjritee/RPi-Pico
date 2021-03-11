
# This experiment is like cp_experiments/shift_register/SR74HC595_experiment3.py
# except that, instead of inheriting from the SR74HC595 class I define a class
# similar to SR74HC59 defined in sr74HC595.py but only uses on_pins to set the pins that are on.

# The other difference is that I have defined a DebouncedButton class that
# uses an IRQ callback on the button with debouncing


import machine
import time
import sr74HC595

# This class defines a debounced button using an IRQ callback
class DebouncedButton(machine.Pin):

    # number of retries of the buttons value to determine if the value is stable
    RETRIES = 40
    
    def __init__(self, pinnum, pinupdown, irq, callback):
        # pinnum is the pin number for the button
        # pinupdown is either machine.Pin.PULL_DOWN or machine.Pin.PULL_UP
        # irq is either machine.Pin.IRQ_FALLING  or machine.Pin.IRQ_RISING
        # callback is the user defined callback in response to a debounced button event
        # it has one argument that will be the DebouncedButton (pin) object
        super().__init__(pinnum, machine.Pin.IN, pinupdown)
        # setup an IRQ triggered callback for the button
        self.irq(trigger=irq, handler=self.handler)
        self.callback = callback
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
    
    def handler(self, pin):
        # callback for button
        if self.debounce():
            self.callback(pin)
    
    
num_lights = 1
def callback(pin):
    global num_lights
    num_lights = num_lights % 7 + 1
    
button = DebouncedButton(13, machine.Pin.PULL_DOWN, machine.Pin.IRQ_RISING, callback)

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
                          for offset in range(num_lights))
        
            delay = potentiometer.read_u16()/200000
            time.sleep(delay)
 

if __name__ == "__main__":
    main()