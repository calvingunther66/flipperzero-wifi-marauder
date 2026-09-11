#!/usr/bin/env python3
"""
Test storage list command with path
"""

import serial
import time
import sys
import os

def test_storage_list():
    port = '/dev/tty.usbmodemflip_Korgisap1'
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Connected to {port}")
        
        # Clear buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Wait a bit
        time.sleep(0.5)
        
        # List /ext/apps/
        print("Sending 'storage list /ext/apps/\\r\\n'...")
        ser.write(b"storage list /ext/apps/\r\n")
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
        print(f"Full response: {repr(full_text)}")
        
        # Look for marauder in the response
        if 'marauder' in full_text.lower():
            print("Found marauder in storage!")
        else:
            print("Marauder not found in /ext/apps/ listing")
            
        # Also check internal storage
        print("\nSending 'storage list /int/\\r\\n'...")
        ser.reset_input_buffer()
        ser.write(b"storage list /int/\r\n")
        ser.flush()
        
        all_data2 = []
        start_time = time.time()
        while time.time() - start_time < 5:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if data:
                    text = data.decode('utf-8', errors='ignore')
                    all_data2.append(text)
                    print(f"Received: {repr(text)}")
            time.sleep(0.1)
        
        full_text2 = ''.join(all_data2)
        print(f"/int/ listing: {repr(full_text2)}")
        if 'marauder' in full_text2.lower():
            print("Found marauder in internal storage!")
        
        ser.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_storage_list()
