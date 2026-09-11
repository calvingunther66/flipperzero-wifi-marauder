#!/usr/bin/env python3
"""
Check if we can detect when marauder is actually running
"""

import serial
import time
import sys
import os

def check_if_running():
    port = '/dev/tty.usbmodemflip_Korgisap1'
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Connected to {port}")
        
        # Clear buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Wait for initial prompt
        time.sleep(1)
        
        # Get baseline
        print("Getting baseline Flipper prompt...")
        ser.write(b"help\r\n")
        ser.flush()
        time.sleep(1)
        
        baseline_prompt = ""
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            baseline_prompt = data.decode('utf-8', errors='ignore')
            print(f"Baseline ends with: {repr(baseline_prompt[-20:])}")
        
        # Now try to start marauder by going through the GPIO menu
        print("\n--- Navigating to GPIO menu ---")
        ser.reset_input_buffer()
        ser.write(b"GPIO\r\n")
        ser.flush()
        time.sleep(1)
        
        gpio_response = ""
        start_time = time.time()
        while time.time() - start_time < 2:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if data:
                    text = data.decode('utf-8', errors='ignore')
                    gpio_response += text
                    print(f"[{time.time()-start_time:.3f}s] GPIO: {repr(text)}")
            time.sleep(0.05)
        
        print(f"GPIO full response: {repr(gpio_response)}")
        
        # If we see a menu, try to find marauder in it
        if 'In-Development' in gpio_response:
            print("Found In-Development menu, trying to enter it...")
            ser.reset_input_buffer()
            ser.write(b"In-Development\r\n")
            ser.flush()
            time.sleep(1)
            
            id_response = ""
            start_time = time.time()
            while time.time() - start_time < 2:
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting)
                    if data:
                        text = data.decode('utf-8', errors='ignore')
                        id_response += text
                        print(f"[{time.time()-start_time:.3f}s] In-Dev: {repr(text)}")
                time.sleep(0.05)
            
            print(f"In-Dev full response: {repr(id_response)}")
            
            # Look for marauder in the listing
            if 'marauder' in id_response.lower():
                print("Found marauder in In-Development menu!")
                # Try to select it
                ser.reset_input_buffer()
                ser.write(b"esp32_wifi_marauder\r\n")
                ser.flush()
                time.sleep(2)
                
                launch_response = ""
                start_time = time.time()
                while time.time() - start_time < 3:
                    if ser.in_waiting > 0:
                        data = ser.read(ser.in_waiting)
                        if data:
                            text = data.decode('utf-8', errors='ignore')
                            launch_response += text
                            print(f"[{time.time()-start_time:.3f}s] Launch: {repr(text)}")
                    time.sleep(0.05)
                
                print(f"Launch response: {repr(launch_response)}")
                
                # Now check if we're at a different prompt
                time.sleep(1)
                ser.reset_input_buffer()
                ser.write(b"\r\n")
                ser.flush()
                time.sleep(0.5)
                
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting)
                    if data:
                        text = data.decode('utf-8', errors='ignore')
                        print(f"Prompt test: {repr(text)}")
                        
                        # Check if this looks like a marauder prompt
                        if ':>' in text or text.strip() == '' or ('>' in text and 'marauder' in text.lower()):
                            print("SUCCESS: Appears to be at marauder prompt!")
                            return True
        
        ser.close()
        return False
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if check_if_running():
        print("\n=== MARAUDER APPEARS TO BE RUNNING ===")
    else:
        print("\n=== Could not confirm marauder is running ===")
