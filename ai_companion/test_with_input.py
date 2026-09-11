#!/usr/bin/env python3
"""
Test sending input and seeing what we get back
"""

import serial
import time
import sys
import os

def test_with_input():
    port = '/dev/tty.usbmodemflip_Korgisap1'
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Connected to {port}")
        
        # Clear buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Wait for initial prompt
        time.sleep(1)
        
        # Send a command and see response
        print("Sending 'help\\r\\n'...")
        ser.write(b"help\r\n")
        ser.flush()
        
        # Collect response for 3 seconds
        start_time = time.time()
        all_data = []
        
        while time.time() - start_time < 3:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if data:
                    text = data.decode('utf-8', errors='ignore')
                    all_data.append(text)
                    print(f"[{time.time()-start_time:.3f}s] Received: {repr(text)}")
            time.sleep(0.05)
        
        full_text = ''.join(all_data)
        print(f"\nFull response: {repr(full_text)}")
        
        # Now try to run marauder app
        print("\n--- Trying to run marauder app ---")
        ser.reset_input_buffer()
        ser.write(b"app run esp32_wifi_marauder\r\n")
        ser.flush()
        
        all_data2 = []
        start_time = time.time()
        marauder_found = False
        
        while time.time() - start_time < 5:  # Wait 5 seconds
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if data:
                    text = data.decode('utf-8', errors='ignore')
                    all_data2.append(text)
                    print(f"[{time.time()-start_time:.3f}s] Received: {repr(text)}")
                    
                    # Check if we see marauder indicators
                    if ':>' in text or 'marauder' in text.lower():
                        print(">>> MARAUDER PROMPT DETECTED! <<<")
                        marauder_found = True
            time.sleep(0.05)
        
        full_text2 = ''.join(all_data2)
        print(f"\nFull marauder response: {repr(full_text2)}")
        
        if marauder_found:
            print("SUCCESS: Marauder app is running!")
        else:
            print("Marauder app did not start or we didn't detect the prompt")
        
        ser.close()
        return marauder_found
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_with_input()
