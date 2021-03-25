# This experiment uses a very simple PIO program that sets LEDs on/off and is used
# to cycle through 8 LEDs in the same way as the shift_register experiments but is way simpler -
# we simply write 8 bits to the state machine (representing the state of the 8 LEDs)
# and in the state machine pull the input and use the first 8 bits to set the pins
import time
import board
import digitalio
import rp2pio
import adafruit_pioasm

button = digitalio.DigitalInOut(board.GP16)
button.switch_to_input(pull=digitalio.Pull.DOWN)

set_leds = """
.program set_leds

pull
out pins 8   ; set pins using the first 8 bits pulled
"""

assembled = adafruit_pioasm.assemble(set_leds)

# The LEDs are connected to pins in order starting with GP2
# i.e. GP2, GP3, ..., GP9
sm = rp2pio.StateMachine(
    assembled,
    frequency=2000,
    first_out_pin=board.GP2, # start out pin
    out_pin_count = 8,       # number of out pins
)

# onpins is a sequence of pin numbers (1,2,..., 8)
# that are to be set on
def set_LEDs(onpins):
    pins = 0
    for p in onpins:
        pins |= 1 << (p % 8)
    # pins is an int whose set bits represent the LEDs to be set on
    # and this is written to the state machine
    sm.write(bytes((pins,)))
    
def main():
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
    
            set_LEDs((index+offset for offset in range(num_lights)))
        
            time.sleep(0.3)
 

if __name__ == "__main__":
    main()