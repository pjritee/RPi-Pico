# Quick and dirty tkinter app for displaying temperature and humidity data
# sent via serial communication
# I have hard wired the serial port to be '/dev/ttyUSB0'
# If you are using a Linux machine - eg an RPi then plug the USB end
# of the serial cable into your machine and then in a terminal type
# dmesg
# and you will see something like
# cp210x converter now attached to ttyUSB0
# near the bottom of the output


# !!! WARNING !!!
# When I run this on my Linux box and I unplug the USB for the serial connection
# my box completely freezes and I need to do a hard reboot.
# I am guessing that it's because the program is blocked on a readline
# but completely freezing seems a bit extreme.
# No idea how to fix this.

import serial
import queue as Queue
import tkinter as tk
import threading
import json
import time

message_queue = Queue.Queue()

class SerialReader(threading.Thread):
    def __init__(self, app):
        self.conn = serial.Serial('/dev/ttyUSB0', baudrate = 115200)
        self.app = app
        self.running = True
        threading.Thread.__init__(self)
        self.daemon = True
 
    def run(self):
        while (self.running):
            try:
                msg = self.conn.readline().decode()
                message_queue.put(msg)
                self.app.master.event_generate("<<data>>")
            except Exception as e:
                print("Serial Reader Exception:", str(e))
                self.conn.close()
                break

    def stop(self):
        # close serial comm on shutdown
        self.conn.close()
        self.running = False

class WeatherApp(object):

    def __init__(self, master):
        master.title("")
        master.protocol("WM_DELETE_WINDOW", self.closeEvent)
        self.master = master
        self.temperature_label = tk.Label(master,text="Temperature: ----")
        self.temperature_label.pack()
        self.humidity_label = tk.Label(master,text="Relative Humidity: ----")
        self.humidity_label.pack()
        self.reader = SerialReader(self)
        self.reader.start()
        self.master.bind("<<data>>", self.data_message)

    def closeEvent(self):
        self.reader.stop()
        # give time for the comms to close before destroying the app
        time.sleep(0.2)
        self.master.destroy()

    def data_message(self, _):
        try:
            data = message_queue.get()
            data_dict = json.loads(data)
            self.temperature_label.config(text = f'Temperature: {data_dict["temperature"]}C')
            self.humidity_label.config(text = f'Relative Humidity: {data_dict["relative_humidity"]}%')
        except Exception as e:
            print("data_message Exception:", str(e))
        

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()


