#!/usr/bin/env python3
"""
Test menu navigation
"""

import serial
import time
import sys
import os

def test_menu():
    port = '/dev/tty.usbmodemflip_Korgisap1'
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Connected to {port}")
        
        # Clear buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Wait for initial prompt
        time.sleep(1)
        
        # Let's see what happens when we just press enter a few times
        print("=== Testing basic interaction ===")
        for i in range(3):
            ser.write(b"\r\n")
            ser.flush()
            time.sleep(0.5)
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if data:
                    text = data.decode('utf-8', errors='ignore')
                    print(f"[{i}] Response: {repr(text)}")
        
        # Now let's try to see if we can get a listing of something
        print("\n=== Trying to see what's available ===")
        ser.write(b"ls\r\n")
        ser.flush()
        time.sleep(1)
        
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            if data:
                text = data.decode('utf-8', errors='ignore')
                print(f"ls response: {repr(text)}")
        
        ser.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_menu()
