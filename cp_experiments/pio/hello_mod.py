# SPDX-FileCopyrightText: 2021 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Adapted from the example https://github.com/raspberrypi/pico-examples/tree/master/pio/hello_pio

# In this experiment I have modified the program linked above to use 2 LEDs and flip back and
# forward between the two
# To help in my understanding I have added comments that start with ; ? or # ?
# The ? is becauuse I'm not sure
import time
import board
import rp2pio
import adafruit_pioasm

hello = """
.program hello
loop:
; ? wait for and then read data into the Output Shift Register
    pull
; ? In the original code we read one bit but here we read 2 bits - one bit for each pin
; ? The two pins are set based on the 2 bits read - e.g. 01 sets GP19, 10 sets GP20 and 11 sets both
    out pins, 2
; This program uses a 'jmp' at the end to follow the example.  However,
; in a many cases (including this one!) there is no jmp needed at the end
; and the default "wrap" behavior will automatically return to the "pull"
; instruction at the beginning.
; ? It also appears that the loop: label is not needed - if I comment out both
; ? loop:  and jmp loop  then the program works the same.
; ? That suggests the state machine is, itself, running in a loop
    jmp loop
"""

# ?run the assembler on the above program and return an assembled object
assembled = adafruit_pioasm.assemble(hello)

# ? start the state machine
# ? assembled is the assembled code object
# ? frequency gives the rate at which instructions are executed
# ?   because the state machine is blocking on a pull and then sleeping for 0.5 secs
# ?   then the choice of frequency doesn't matter because the program will run at "full speed"
# ?   because it's the sleeping that determines the speed. Note that 2000 is close to the lowest
# ?   allowed frequency.
# ? first_out_pin is the first pin (in sequence) to be used for output
# ? out_pin_count is the number of output pins being used
# ?   this defaults to 1 and if I comment that out I get the error
# ?       ValueError: Instruction 1 shifts out more bits than pin count
# ?   It's OK to shift out less bits than the pin count
sm = rp2pio.StateMachine(
    assembled,
    frequency=2000,
    first_out_pin=board.GP19,
    out_pin_count = 2,
)
print("real frequency", sm.frequency)

while True:
    # ? write 0x01 to the state machine (to be pulled by the first instruction)
    # ? will turn on the LED on GP19
    sm.write(bytes((1,)))
    time.sleep(0.5)
    # ? write 0x02 to the state machine
    # ? will turn on the LED on GP20
    sm.write(bytes((2,)))
    time.sleep(0.5)
