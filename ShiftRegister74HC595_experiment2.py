#
# This is a variation on ShiftRegister74HC595_experiment.py
# The first change is, when you press the button, you don't have to wait for a complete
# cycle for the number of lights to change.
# The more important change is the use of gpio.
# My understanding from looking at what happens is that whenever you do, for example,
# pins[index].value = True
# then there will be a communication via spi with a number representing which bits will be set
# (posssibly only if this flipped the value).
# This means each time around the loop there will be num_lights+1 communications.
# This version does, I believe, only one communication each time around the loop by
# putting the number representing the required bit pattern in gpio
import board
import digitalio
import adafruit_74hc595
import busio
import time
import analogio

button = digitalio.DigitalInOut(board.GP13)
button.switch_to_input(pull=digitalio.Pull.DOWN)

latch_pin =  digitalio.DigitalInOut(board.GP6)
latch_pin.direction = digitalio.Direction.OUTPUT

potentiometer = analogio.AnalogIn(board.GP26)
   
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3)

spi.try_lock()
spi.configure(baudrate=5000000, phase=0, polarity=0)
spi.unlock()

sr = adafruit_74hc595.ShiftRegister74HC595(spi, latch_pin)

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
    
        # initialise the bit pattern to all zeros 
        pins = 0
        for offset in range(num_lights):
            # set the required bit to 1
            pins |= 1 << ((index+offset) % 8)
        # send off that bit pattern
        sr.gpio = pins
        
        delay = potentiometer.value/200000
        time.sleep(delay)
        
