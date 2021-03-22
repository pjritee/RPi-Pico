
# using a common anode RGB
# because it is a common anode then the brightness is "inverted"
# so duty_u16(0) is maximum brightness and
# duty_u16(2**16-1) is off
# see, for example, http://www.pibits.net/code/raspberry-pi-pico-and-rgb-led-example-in-micropython.php
# The longest pin on the common anode RGB is connected to 3V

from machine import Pin,PWM

red = PWM(Pin(19, Pin.OUT))
green = PWM(Pin(20, Pin.OUT))
blue = PWM(Pin(21, Pin.OUT))

red.freq(1000)
green.freq(1000)
blue.freq(1000)


SCALE = (2**16 - 1)/255

# convert from a colour in 0..255 to the required duty cycle value

def duty(v):
    return int((255 - v % 256) * SCALE)

red.duty_u16(duty(0))
green.duty_u16(duty(0))
blue.duty_u16(duty(0))

# rgb takes either an RGB triple like (255, 0, 255)
# or a hex string like '#ff00ff'

def rgb(value):
    if type(value) == type(''):
        red_val = int(value[1:3], 16)
        green_val = int(value[3:5], 16)
        blue_val = int(value[5:], 16)
    else:
        red_val, green_val, blue_val = value
        
    red.duty_u16(duty(red_val))
    green.duty_u16(duty(green_val))
    blue.duty_u16(duty(blue_val))