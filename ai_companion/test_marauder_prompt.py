#!/usr/bin/env python3
"""
Test to find the actual marauder prompt
"""

import serial
import time
import sys
import os

def test_marauder_prompt():
    port = '/dev/tty.usbmodemflip_Korgisap1'
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Connected to {port}")
        
        # Clear buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Wait for initial prompt
        time.sleep(1)
        
        # First, let's see what the normal prompt looks like
        print("Getting baseline prompt...")
        ser.write(b"?\r\n")  # help command
        ser.flush()
        time.sleep(1)
        
        baseline = ""
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            baseline = data.decode('utf-8', errors='ignore')
            print(f"Baseline response: {repr(baseline)}")
        
        # Now let's try to load the marauder app properly
        # Based on the flipper OS, we might need to use 'load' or go through menus
        print("\n--- Trying to load marauder via storage/run ---")
        ser.reset_input_buffer()
        ser.write(b"storage run /ext/apps/esp32_wifi_marauder.fap\r\n")
        ser.flush()
        
        marauder_response = ""
        start_time = time.time()
        while time.time() - start_time < 5:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if data:
                    text = data.decode('utf-8', errors='ignore')
                    marauder_response += text
                    print(f"[{time.time()-start_time:.3f}s] Received: {repr(text)}")
            time.sleep(0.05)
        
        print(f"\nFull marauder load response: {repr(marauder_response)}")
        
        # Look for the actual marauder prompt - it should be different from the flipper prompt
        # The flipper prompt is "> "
        # The marauder prompt might be something like "> " or "marauder> " or just ":>"
        
        if 'marauder' in marauder_response.lower():
            print("Found 'marauder' in response")
        
        # Check if prompt changed
        if marauder_response.endswith(':>') or 'marauder> ' in marauder_response:
            print("MARAUDER PROMPT DETECTED!")
        elif '> ' in marauder_response and not baseline.endswith('> '):
            print("Prompt changed - possibly marauder running")
        
        ser.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_marauder_prompt()
