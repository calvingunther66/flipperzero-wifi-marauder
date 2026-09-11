#!/usr/bin/env python3
"""
Test sending marauder command and seeing the response
"""

import serial
import time
import sys
import os

def test_marauder():
    port = '/dev/tty.usbmodemflip_Korgisap1'
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Connected to {port}")
        
        # Clear buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Wait a bit for anything
        time.sleep(0.5)
        
        # Send marauder command
        print("Sending 'marauder\\r\\n'...")
        ser.write(b"marauder\r\n")
        ser.flush()
        
        # Wait and collect response
        start_time = time.time()
        all_data = []
        
        while time.time() - start_time < 8:  # Wait 8 seconds
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if data:
                    text = data.decode('utf-8', errors='ignore')
                    all_data.append(text)
                    print(f"Received: {repr(text)}")
            time.sleep(0.1)
        
        print(f"\nTotal chunks: {len(all_data)}")
        full_text = ''.join(all_data)
        print(f"Full response: {repr(full_text)}")
        
        # Check if we see the marauder prompt
        if 'marauder' in full_text.lower():
            print("Found 'marauder' in response!")
        if ':>' in full_text:
            print("Found Marauder prompt ':>'")
        if '> ' in full_text:
            print("Found regular prompt '> '")
            
        ser.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_marauder()
