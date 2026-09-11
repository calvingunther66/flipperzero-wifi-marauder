#!/usr/bin/env python3
"""
Test script to figure out how to properly communicate with Marauder
"""

import serial
import time
import sys
import os

# Add the ai_companion directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from serial_comm import FlipperSerial

def test_direct_communication():
    """Test direct communication to understand the protocol"""
    print("Testing direct communication with Flipper Zero...")
    
    flipper = FlipperSerial('/dev/tty.usbmodemflip_Korgisap1')
    if not flipper.connect():
        print("Failed to connect")
        return
    
    flipper.start_reading()
    time.sleep(0.5)
    
    # Clear any existing data
    flipper.serial_conn.reset_input_buffer()
    flipper.serial_conn.reset_output_buffer()
    
    # Let's see what we get with just a newline
    print("\n=== Sending newline ===")
    flipper.send_command("")
    time.sleep(0.5)
    response = flipper.read_response(timeout=2)
    print(f"Response: {repr(response)}")
    
    # Try to get to marauder app
    print("\n=== Trying to launch marauder ===")
    flipper.send_command("marauder")
    time.sleep(2)  # Wait longer for app to load
    response = flipper.read_response(timeout=3)
    print(f"After 'marauder' command: {repr(response)}")
    
    # Try some known marauder commands
    print("\n=== Trying scanap ===")
    flipper.send_command("scanap")
    time.sleep(5)  # Give time for scan
    response = flipper.read_response(timeout=8)
    print(f"ScanAP response: {repr(response)}")
    
    # Try to see if we get any different response
    print("\n=== Trying help ===")
    flipper.send_command("help")
    time.sleep(1)
    response = flipper.read_response(timeout=3)
    print(f"Help response: {repr(response)}")
    
    flipper.disconnect()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    test_direct_communication()
