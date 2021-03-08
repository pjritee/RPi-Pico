# Experiments with Serial Communication

## Serial Communication over the USB connection to access a temperature/humidity sensor
The files are:
- am2320_to_serial_experiment.py: this is the Pico side of the experiment and follows https://learn.adafruit.com/adafruit-am2320-temperature-humidity-i2c-sensor/python-circuitpython using the RPi wiring except, because the Pico provides several I2C buses, I chose the one using GP8 (I2C0SDA) and GP9 (I2C0SCL)
- serial_interface.py: this defines a class for communicating with the Pico asking for temperature and humidity values
- serial_to_am2320_experiment.py: This uses the above class - every 5 secs it prints out the temperature and humidity values

### Problems with serial comminication over USB
I currently don't have suitable cables to, for examplle, use UART so I thought I'd try communication over USB but, as I discovered, it has an issue. Perhaps, in hindsight, this was an obvious issue. It all comes down to how Thonny (or whatever) interacts with Pico. To support this connection circuitpython maps standard input/output to the USB serial connection so reading and writing in Python programs on the Pico become serial communication to, for example, Thonny.

For the REPL in Thonny, for example, an expression is sent over the serial line so that the circuitpython REPL can evaluate that expression. I made the mistake of thinking that when I pressed a RETURN after entering an expression that expression would be sent and was taken aback when the expression string was echoed.  After thinking about this I think I now understand what is happening. Because we want to use command line editing and history in the Thonny REPL then there seems to be two options: to do the command line editing and history on the Thonny side or to do it on the Pico side. If we do it on the Thonny side then we would have to use the readline library on that side and write lots of support code. On the other hand circuitpython has readline support builtin and so it's more efficient to use that. A consequences of this is that as the keystrokes are sent to the Pico side the Pico side needs to respond to command line editing and history "commands" and send back the current (edited) expression so that the user gets the same experience as though they were doing the command line editing and history locally.

This means, for my experiment, I needed to ignore echoed text and I did this by having the Pico side send back a particular string that I could use a regular expression on to extract the data from the "noise". I don't know if there is a better way of doing it.

Related to this, if you want to experiment with this code you need to copy am2320_to_serial_experiment.py to code.py on the Pico, make sure Thonny is not running, and unplug/plug the USB in your computer.