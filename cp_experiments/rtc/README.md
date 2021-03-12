# Real Time Clock Experiment

`rtc.py` is a very simple experiment using a DS3231 real time clock connected to the Pico via I2C.

Because CircuitPython has different aims to MicoPython - in particular trying to be as user-friendly for beginners as possible it does lack support (I believe) for threading, timers etc. and so that makes an RTC less useful than in MicroPython.

This is not meant to be a criticism of CircuitPython - quite the opposite in fact - I found the library support and tutorials supplied by Adafruit to be very helpful in getting me up and running.
