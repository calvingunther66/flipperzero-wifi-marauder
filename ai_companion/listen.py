#!/usr/bin/env python3
"""
Just listen to the serial port for a few seconds
"""

import serial
import time
import sys
import os

def listen():
    port = '/dev/tty.usbmodemflip_Korgisap1'
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Listening on {port}...")
        start = time.time()
        while time.time() - start < 5:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if data:
                    text = data.decode('utf-8', errors='ignore')
                    print(repr(text), end='', flush=True)
            time.sleep(0.1)
        print("\nDone listening.")
        ser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    listen()
