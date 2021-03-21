import serial
import json
import threading

conn = serial.Serial('/dev/ttyUSB0', baudrate = 115200)

while True:
    try:
        msg = conn.readline().decode()
        print(msg)
    except Exception as e:
        print("Serial Exception:", str(e))
        conn.close()
        break
