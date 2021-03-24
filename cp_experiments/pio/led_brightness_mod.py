# SPDX-FileCopyrightText: 2021 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Adapted from the an example in Appendix C of RPi_PiPico_Digital_v10.pdf

# This is a small modification to the program linked above -
# only changes are to use GP19 ad GP20 and have the brightness level
# in one the reverse of the other and to add extra comments

import time
import board
import rp2pio
import adafruit_pioasm

# ? pin GP19 quater brightness and GP20 full brightness
led_quarter_brightness = adafruit_pioasm.assemble(
"""
    set pins, 2 [2]
    set pins, 3
"""
)

# ? both half brightness
led_half_brightness = adafruit_pioasm.assemble(
    """
    set pins, 0
    set pins, 3
"""
)

#? pin GP19 full brightness and GP20 quater brightness
led_full_brightness = adafruit_pioasm.assemble(
    """
    set pins, 1 [2]
    set pins, 3
    
"""
)

while True:
    # ? I wondered if we couldn't construct 3 machines before the loop
    # ? and then start and stop each in turn.
    # ? the problem is when I tried I got a
    # ?    ValueError: GP20 in use
    # ? when I tried to construct the second machine
    sm = rp2pio.StateMachine(
        led_quarter_brightness, frequency=10000, first_set_pin=board.GP19, set_pin_count = 2
    )
    time.sleep(1)
    # ? essentially deleting the machine - this frees up GP19 for the next machine
    sm.deinit()

    sm = rp2pio.StateMachine(
        led_half_brightness, frequency=10000, first_set_pin=board.GP19, set_pin_count = 2
    )
    time.sleep(1)
    sm.deinit()

    sm = rp2pio.StateMachine(
        led_full_brightness, frequency=10000, first_set_pin=board.GP19, set_pin_count = 2
    )
    time.sleep(1)
    sm.deinit()
