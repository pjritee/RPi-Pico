# This is based on https://learn.adafruit.com/74hc595/usage 
# The code is modified in order to work on the Pico
# The loop has been simplified and then complicated again to
# add a pot and a button

# IC (shift register) pins
# pin 1,13 - ground
# pin 10,16 - 3.3v
# pin 2,3,4,5,6,7,8,15 LED
# pin 11 - pico pin GP2
# pin 12 - pico pin GP6
# pin 14 - pico pin GP3

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
   
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3,
                MISO=board.GP4)

spi.try_lock()
spi.configure(baudrate=5000000, phase=0, polarity=0)
spi.unlock()

sr = adafruit_74hc595.ShiftRegister74HC595(spi, latch_pin)

pins = [sr.get_pin(n) for n in range(8)]

num_lights = 1
button_pressed = False
    
    
while True:
    current_num_lights = num_lights
    for index in range(8):
        # update number of lights if button is pressed
        if button.value and not button_pressed:
            button_pressed = True
            num_lights = num_lights % 7 + 1
        if not button.value and button_pressed:
            button_pressed = False
    
        # cycle through lights
        for offset in range(current_num_lights):    
            pins[(index+offset) % 8].value = True
        pins[index-1].value = False
        delay = potentiometer.value/200000
        time.sleep(delay)
        
