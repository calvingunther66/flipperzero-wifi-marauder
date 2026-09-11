#!/usr/bin/env python3
"""
Simple test to communicate with the Marauder app
"""

import serial
import time
import sys
import os

# Add the ai_companion directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from serial_comm import FlipperSerial
from marauder_controller import MarauderController

def test_simple():
    print("=== Testing Simple Marauder Communication ===")
    
    # Try to connect
    flipper = FlipperSerial('/dev/tty.usbmodemflip_Korgisap1')
    if not flipper.connect():
        print("Failed to connect to Flipper Zero")
        return False
    
    print("Connected to Flipper Zero")
    
    # Start reading thread
    flipper.start_reading()
    time.sleep(0.5)
    
    # Clear buffers
    flipper.serial_conn.reset_input_buffer()
    flipper.serial_conn.reset_output_buffer()
    
    # Try to launch marauder app via RPC or direct command
    print("\n--- Trying to launch Marauder via 'app run esp32_wifi_marauder' ---")
    flipper.send_command("app run esp32_wifi_marauder")
    time.sleep(2)
    
    # Check for response
    if flipper.serial_conn.in_waiting > 0:
        data = flipper.serial_conn.read(flipper.serial_conn.in_waiting)
        if data:
            text = data.decode('utf-8', errors='ignore')
            print(f"Response: {repr(text)}")
    
    # Wait a bit more to see if we get any data
    time.sleep(3)
    if flipper.serial_conn.in_waiting > 0:
        data = flipper.serial_conn.read(flipper.serial_conn.in_waiting)
        if data:
            text = data.decode('utf-8', errors='ignore')
            print(f"Additional response: {repr(text)}")
            
            # Look for marauder prompt
            if ':>' in text or 'marauder' in text.lower():
                print("SUCCESS: Marauder app seems to be running!")
                flipper.disconnect()
                return True
    
    # If that didn't work, try going through the menu
    print("\n--- Trying to navigate via menu ---")
    # Go to GPIO menu
    flipper.send_command("GPIO")
    time.sleep(1)
    
    if flipper.serial_conn.in_waiting > 0:
        data = flipper.serial_conn.read(flipper.serial_conn.in_waiting)
        if data:
            text = data.decode('utf-8', errors='ignore')
            print(f"GPIO response: {repr(text)}")
    
    time.sleep(2)
    if flipper.serial_conn.in_waiting > 0:
        data = flipper.serial_conn.read(flipper.serial_conn.in_waiting)
        if data:
            text = data.decode('utf-8', errors='ignore')
            print(f"After GPIO: {repr(text)}")
    
    flipper.disconnect()
    return False

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    test_simple()
