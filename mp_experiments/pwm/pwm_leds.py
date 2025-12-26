
"""
This is an experiment with 16 independent PWM control_generatorled LEDs on a Raspberry Pi Pico.

From  https://deepbluembedded.com/raspberry-pi-pico-w-pinout-diagram-gpio-guide/ :
The Raspberry Pi Pico has 8 independent PWM generators, called slices. Each slice has two channels (A and B), which gives us a total of 16 PWM channels.
 

Pin mapping:
  0    0A
  1    0B
  2    1A
  3    1B
  4    2A
  5    2B
  22   3A
  7    3B 
  8    4A
  9    4B
  26   5A
  27   5B
  28   6A
  13   6B
  14   7A   
  15   7B
 
"""


from machine import Pin, PWM
import time
import random
import math

MAX_DUTY = 65535
HALF_MAX_DUTY = 32768

leds = [
    PWM(Pin(0)),    # 0A
    PWM(Pin(1)),    # 0B      
    PWM(Pin(2)),    # 1A
    PWM(Pin(3)),    # 1B
    PWM(Pin(4)),    # 2A 
    PWM(Pin(5)),    # 2B
    PWM(Pin(7)),    # 3B
    PWM(Pin(8)),    # 4A
    PWM(Pin(9)),    # 4B    
    PWM(Pin(13)),   # 6B
    PWM(Pin(14)),   # 7A 
    PWM(Pin(15)),   # 7B
    PWM(Pin(26)),   # 5A
    PWM(Pin(27)),   # 5B
    PWM(Pin(28)),   # 6A   
    PWM(Pin(22))    # 3A
    ]

# Initialize PWM frequencies
for led in leds:
    led.freq(1000)	

# PWM generators
# Each generator yields duty cycle values from 0 to 65535
# The supplied length is the number of generated values

# Sine wave generator
def pwm_sin_generator(length):
    delta = 2*math.pi/length # angle step
    for n in range(length):
        yield int((1 +math.sin(n*delta))*HALF_MAX_DUTY)

# Random sine wave generator whose length is randomly chosen from values between low_length and hi_length
def pwm_rand_sin_generator(low_length, hi_length):
    yield from pwm_sin_generator(random.randint(low_length, hi_length))

# Square wave generator
def pwm_square_generator(length):
    half = length//2
    for _ in range(half):
        yield MAX_DUTY
    for _ in range(length - half):
        yield 0

# Random square wave generator whose length is randomly chosen from values between low_length and hi_length 
def pwm_rand_square_generator(low_length, hi_length):
    yield from pwm_square_generator(random.randint(low_length, hi_length))
    
# Sawtooth wave generator
def pwm_sawtooth_generator(length):
    delta = MAX_DUTY/length
    d = HALF_MAX_DUTY
    while d < MAX_DUTY:      # rising edge from half to max
        yield int(d)
        d += delta
    d -= delta
    while d >= 0:            # falling edge from max to 0
        yield int(d)
        d -= delta
    d += delta
    while d < HALF_MAX_DUTY: # rising edge from 0 to half
        yield int(d)
        d += delta

# Random sawtooth wave generator whose length is randomly chosen from values between low_length and hi_length       
def pwm_rand_sawtooth_generator(low_length, hi_length):
    yield from pwm_sawtooth_generator(random.randint(low_length, hi_length))
    

# On and Off generators 
def on_generator(length):
    for _ in range(length):
        yield MAX_DUTY
def off_generator(length):
    for _ in range(length):
        yield 0
        
           
    
# Returns a function that when called returns a generator that repeatedly yields from
# the supplied generator forever
def repeat_generator_always(generator, *args):
    def repeat_generator():
        while True:
            yield from generator(*args)
    return repeat_generator

# Returns a function that when called returns a generator that repeatedly yields from
# the supplied generator for the supplied number of times
def repeat_generator_for(number, generator, *args):
    def repeat_generator():
        for _ in range(number):
            yield from generator(*args)
    return repeat_generator

# Returns a function that when called returns a generator that repeatedly yields from
# the supplied generator with each repeat carried out with the supplied probability 
def repeat_generator_random(probability, generator, *args):
    def repeat_generator():
        while random.randint(0,100) < probability:
            yield from generator(*args)
    return repeat_generator

# A generator that yields the required delay followed by repeatedly making a random choice from
# generator_list and yielding from that generator produced from that choice.
def sequence_choice_generator(generator_list, delay=0):
    if delay > 0:
        yield from off_generator(delay)
    while True:
        yield from random.choice(generator_list)()

# A generator that yields the required delay followed by repeatedly iterating through
# generator_list and yielding from that generator produced from that entry.
def sequence_iterate_generator(generator_list, delay=0):
    if delay > 0:
        yield from off_generator(delay)
    while True:
        for generator in generator_list:
            yield from generator()
        
        
# Example generator sequences for each LED
generators = [
    # A random square wave whose length is between 100 and 200 steps, with a 20% chance of repeating
    repeat_generator_random(20, pwm_rand_square_generator, 100, 200),
    # A sine wave  whose length is between 200 and 600 steps, with a 70% chance of repeating
    repeat_generator_random(70, pwm_rand_sin_generator, 200, 600),
    # An on generator for 100 steps with a 25% chance of repeating
    repeat_generator_random(25, on_generator, 100)
    ]

# Create a list of pairs each consisting of a led and a generator to be used for that led with each generator being a choice generator using 
# a random delay between 20 and 200 steps to stagger the starting times
led_controls = [(led, sequence_choice_generator(generators, delay=random.randint(20,200))) for led in leds]
       
# As an alternative example the following setup will have each lead pulsing in the same sin wave pattern but with an increasing
# offset. The first LED starts immediately, the second after 20 steps, the third after 40 steps etc.
# led_controls = [(led, sequence_choice_generator([repeat_generator_always(pwm_sin_generator, 400)], delay=i*20)) for i, led in enumerate(leds)]

# Initialize all LEDs to off
for led in leds:
    led.duty_u16(0)
    
while True:
    time.sleep_ms(5)
    # Each step takes about 5ms and so, for example, a sine wave of length 400 will have a period of about 2 seconds.

    # update each LED's duty cycle from its generator
    for led, gen in led_controls:
        led.duty_u16(next(gen))
    