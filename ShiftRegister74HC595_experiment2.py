#
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
    
        pins = 0
        for offset in range(num_lights):
            pins |= 1 << ((index+offset) % 8)
        sr.gpio = pins
        
        delay = potentiometer.value/200000
        time.sleep(delay)
        
