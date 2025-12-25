# Using 16 PWM channels on a Raspberry Pi Pico to independently drive LEDs

The aim of this experiment is to control_generator 16 LEDs independently using appropriate PWM channels (pins).

The choices of pins to get 16 independent PWM channels was determined follwing 
 https://deepbluembedded.com/raspberry-pi-pico-w-pinout-diagram-gpio-guide/.

 It would have been more convinient for this experiment if there was a more even distribution of suitable pins on the left and right of the Pico but that was not to be.

 The wiring is straightforward with the positive side of each LED connected to a pin and the negative side connected to a 200K resistor which in turn is connected to ground.

 I 3D printed some covers using clear filament as an amusement and found that they produced suprisingly pleasent effects. I think this was partly due to way the light interacted with the 3D print layers. See youtube for an example run of the system. THe Youtube video doesn't really do it justice.

