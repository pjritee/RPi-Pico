
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
        
           


    
def apply_next(control_generator, led):
    d = next(control_generator)
    led.duty_u16(d)
    
""" LED control class
    Each instance controls one LED according to a sequence of generator functions.

    Each generator function is specified along with its arguments and a repeat count.
    Each time a generator is chosen (including as a repeat) the generator function is called with the supplied arguments 
    to create a new generator instance.

    The repeat count can be:
     > 0 : repeat this many times
     = 0 : repeat forever (no other generators in the sequence will be used once this one is reached/chosen)
     < 0 : -repeat is the percentage chance of repeating (e.g. -20 means 20% chance of repeating)

    delay: if > 0, the LED is kept off for this many steps before starting the generator sequence.

    choose: if choose is True, then each time a new generator is needed, one is chosen randomly from the sequence.
 """

class LedControl:
    def __init__(self, led, generator_sequence, delay = 0, choose=False):
        self.led = led
        self.generator_sequence = generator_sequence
        self.len = len(generator_sequence)
        self.index = 0
        self.choose = choose
        self.another_repeat = False
        if choose:
            self.generator_function, self.args, self.repeat = random.choice(self.generator_sequence)
        else:
            self.generator_function, self.args, self.repeat = generator_sequence[0]
        if delay == 0:
            self.set_control_generator()
        else:
            self.control_generator = off_generator(delay)
     
    # Initialize the control generator according to current index or randomly (if choose is True)
    def set_control_generator(self):
        # reset another_repeat flag. This will only be set to False again if repeat > 0 and runs out
        self.another_repeat = True
        if self.choose:
            self.generator_function, self.args, self.repeat = random.choice(self.generator_sequence)
            self.control_generator = self.generator_function(*self.args)
            return
        
        # sequential choice
        if self.index == self.len:
            # back to the beginning of generator_sequence
            self.index = 0
        self.generator_function, self.args, self.repeat = self.generator_sequence[self.index]
        self.control_generator = self.generator_function(*self.args)
        # move to next index for next time
        self.index += 1            
        
    def step(self):
        try:
            # Get next value from current control generator and apply to LED
            self.led.duty_u16(next(self.control_generator)) 
        except StopIteration:
            # Current control generator is exhausted

            if self.repeat < 0:
                # -self.repeat is the percentage of repeating
                if (random.randint(0,99) < -self.repeat and random.randint(0,100) <= -self.repeat):
                    # repeat
                    self.control_generator = self.generator_function(*self.args)
                    self.led.duty_u16(next(self.control_generator))
                    return
            if self.repeat > 0:
                # repeat again
                self.repeat -= 1
                if self.repeat == 0:
                    # no more repeats
                    self.another_repeat = False
                self.control_generator = self.generator_function(*self.args)
                self.led.duty_u16(next(self.control_generator))
                return
            if self.another_repeat:
                # repeat again
                self.control_generator = self.generator_function(*self.args)
                self.led.duty_u16(next(self.control_generator))
                return
             
            # move on to next in generator_sequence
            self.set_control_generator()
            self.led.duty_u16(next(self.control_generator))
            
                
# Example generator sequences for each LED
generators = [
    # A random square wave whose length is between 100 and 200 steps, with a 20% chance of repeating
    (pwm_rand_square_generator, [100, 200], -20),
    # A sine wave  whose length is between 200 and 600 steps, with a 70% chance of repeating
    (pwm_rand_sin_generator, [200, 600], -70),
    # An on generator for 100 steps with a 25% chance of repeating
    (on_generator, [100], -25)
    ]

# Create a LedControl instance for each LED with a random delay between 20 and 200 steps 
# to stagger the starting times and where each time a new generator is needed, one is chosen randomly from the generators list
control_generators = [LedControl(led, generators, delay=random.randint(20,200), choose=True) for led in leds]
       
# As an alternative example the following setup will have each lead pulsing in the same sin wave pattern but with an increasing
# offset. The first LED starts immediately, the second after 20 steps, the third after 40 steps etc.
# control_generators = [LedControl(led, [(pwm_sin_generator, [300], 0)], delay=i*20) for i, led in enumerate(leds)]

# Initialize all LEDs to off
for led in leds:
    led.duty_u16(0)
    
while True:
    time.sleep_ms(5)
    # Each step takes about 5ms and so, for example, a sin wave of length 400 will have a period of about 2 seconds.
    
    # Step each control generator
    for c in control_generators:
        c.step()
    