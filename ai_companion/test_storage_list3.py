#!/usr/bin/env python3
"""
Test storage list in sub-directories
"""

import serial
import time
import sys
import os

def test_storage_list(path):
    port = '/dev/tty.usbmodemflip_Korgisap1'
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Connected to {port}")
        
        # Clear buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Wait a bit
        time.sleep(0.5)
        
        print(f"Sending 'storage list {path}\\r\\n'...")
        ser.write(f"storage list {path}\r\n".encode())
        ser.flush()
        
        # Wait and collect response
        start_time = time.time()
        all_data = []
        
        while time.time() - start_time < 5:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if data:
                    text = data.decode('utf-8', errors='ignore')
                    all_data.append(text)
                    print(f"Received: {repr(text)}")
            time.sleep(0.1)
        
        print(f"\nTotal chunks: {len(all_data)}")
        full_text = ''.join(all_data)
        print(f"Full response for {path}: {repr(full_text)}")
        
        # Look for marauder in the response
        if 'marauder' in full_text.lower():
            print("Found marauder in storage!")
            return True
        else:
            print("Marauder not found")
            return False
        
        ser.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Check various directories
    dirs = [
        "/ext/apps/Games",
        "/ext/apps/In-Development", 
        "/ext/apps/Tools",
        "/ext/apps/Scripts"
    ]
    
    found = False
    for d in dirs:
        print(f"\n=== Checking {d} ===")
        if test_storage_list(d):
            found = True
            break
    
    if not found:
        print("\nMarauder not found in any checked directories")
