#  Experiments with the Programmable I/O  (PIO)

The files `blink_mod.py`, `hello_mod.py` and `led_brightness_mod.py` are small modifications of the example programs in https://learn.adafruit.com/intro-to-rp2040-pio-with-circuitpython/overview . The description of the code on this site is well worth a read.
I have added extra comments to help in my understanding of what's going on.

`led_cycle.py`: This solves the same problem as the LED cycle in the shift register experiments but is way simpler. Video link: https://youtu.be/XEVpcgEZbhc .In hindsight this is a very silly experiment. One of the points of the shift register is that it frees up pins (8 pins added, 3 used) which, of course, this experiment doesn't. Also, it's even easier to just set the pins directly. I guess it's a case of "to a PIO hammer everything is a nail"
