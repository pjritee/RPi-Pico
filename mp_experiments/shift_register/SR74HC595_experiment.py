
import machine
import time
import sr74HC595


button = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)

latch_pin =  machine.Pin(6, machine.Pin.OUT)

#potentiometer = analogio.AnalogIn(board.GP26)
   
#spi = busio.SPI(clock=board.GP2, MOSI=board.GP3)

spi = machine.SPI(0, baudrate=5000000, polarity=0, phase=0,
                  sck=machine.Pin(2), mosi=machine.Pin(3),
                  bits=8)

sr = sr74HC595.SR74HC595(spi, latch_pin)

def main():
    num_lights = 1
    button_pressed = False
    
    while True:
        for index in range(8):
            # update number of lights if button is pressed
            if button.value() and not button_pressed:
                button_pressed = True
                num_lights = num_lights % 7 + 1
            if button.value() == 0 and button_pressed:
                button_pressed = False
    
            sr.on_pins = (index+offset \
                          for offset in range(num_lights))
        
            delay = 1 #potentiometer.value/200000
            time.sleep(delay)
 

if __name__ == "__main__":
    main()