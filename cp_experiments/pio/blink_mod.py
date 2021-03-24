# SPDX-FileCopyrightText: 2021 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Adapted from the example https://github.com/raspberrypi/pico-examples/tree/master/pio/pio_blink

# a copy of the program in the link above with extra comments added (and using GP19)
# I also added a little code to convince myself that the machine was indeed
# "running in the background"

import array
import time
import board
import rp2pio
import adafruit_pioasm

blink = adafruit_pioasm.assemble(
    """
.program blink
    ; ? I don't understand what the block is for it seems that pull by itself is enough
    pull block    ; These two instructions take the blink duration
    ; all 32 bits pulled into the OSR are transfered into register y
    out y, 32     ; and store it in y
forever:
    mov x, y
    set pins, 1   ; Turn LED on
lp1:
    jmp x-- lp1   ; Delay for (x + 1) cycles, x is a 32 bit number
    mov x, y
    set pins, 0   ; Turn LED off
lp2:
    jmp x-- lp2   ; Delay for the same number of cycles again
    jmp forever   ; Blink forever!
"""
)


while True:
    for freq in [5, 8, 30]:
        # ? I like the use of with - I presume the teardown code does a deinit
        with rp2pio.StateMachine(
            blink,
            frequency=125_000_000,
            first_set_pin=board.GP19,
            # ? this is so the write below returns immediately
            # ? with this set the for loop below prints numbers
            # ? if this is commented out then the behaviour of this
            # ? program is that it blocks at the write and so doesn't print anything
            # ? and, even worse, doesn't blink with other frequences as the program
            # ? is stuck forever at the sm.write below
            # ? why doesn't the hello program block on the write???
            # ? It's because this program does not loop back to the pull
            # ? whereas the hello program does and there is nothing for it to pull
            # ? and this is the signal for write to return
            wait_for_txstall=False,
        ) as sm:
            # ? The "I" is to make the array vaues unsigned ints
            data = array.array("I", [sm.frequency // freq])
            sm.write(data)
            # ? do some work
            for i in range(6):
                print(i)
                time.sleep(0.5)
        time.sleep(0.5)
