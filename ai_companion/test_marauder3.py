#!/usr/bin/env python3
"""
More detailed test to understand Marauder communication
"""

import serial
import time
import sys
import os

# Add the ai_companion directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from serial_comm import FlipperSerial

def test_detailed_communication():
    """Test communication with more detailed timing and buffering"""
    print("Testing detailed Marauder communication...")
    
    flipper = FlipperSerial('/dev/tty.usbmodemflip_Korgisap1')
    if not flipper.connect():
        print("Failed to connect")
        return
    
    flipper.start_reading()
    time.sleep(0.5)
    
    # Clear buffers
    flipper.serial_conn.reset_input_buffer()
    flipper.serial_conn.reset_output_buffer()
    
    # Enter Marauder app
    print("\n=== Entering Marauder ===")
    flipper.send_command("marauder")
    time.sleep(2)
    
    # Read all available data
    time.sleep(0.5)
    if flipper.serial_conn.in_waiting > 0:
        data = flipper.serial_conn.read(flipper.serial_conn.in_waiting)
        print(f"Raw data after marauder command: {repr(data)}")
        print(f"As text: {data.decode('utf-8', errors='ignore')}")
    
    # Now try version command
    print("\n=== Sending version command ===")
    flipper.serial_conn.reset_input_buffer()  # Clear input buffer
    flipper.send_command("version")
    time.sleep(2)
    
    # Read all available data
    if flipper.serial_conn.in_waiting > 0:
        data = flipper.serial_conn.read(flipper.serial_conn.in_waiting)
        print(f"Raw version data: {repr(data)}")
        text_data = data.decode('utf-8', errors='ignore')
        print(f"Version as text: {repr(text_data)}")
        
        # Look for actual version info in the text
        lines = text_data.split('\n')
        for i, line in enumerate(lines):
            print(f"Line {i}: {repr(line)}")
    
    # Try help command
    print("\n=== Sending help command ===")
    flipper.serial_conn.reset_input_buffer()
    flipper.send_command("help")
    time.sleep(2)
    
    if flipper.serial_conn.in_waiting > 0:
        data = flipper.serial_conn.read(flipper.serial_conn.in_waiting)
        print(f"Raw help data: {repr(data)}")
        text_data = data.decode('utf-8', errors='ignore')
        print(f"Help as text (first 500 chars): {repr(text_data[:500])}")
    
    # Try scanap command with shorter timeout
    print("\n=== Sending scanap command ===")
    flipper.serial_conn.reset_input_buffer()
    flipper.send_command("scanap")
    time.sleep(5)  # Wait for scan
    
    if flipper.serial_conn.in_waiting > 0:
        data = flipper.serial_conn.read(flipper.serial_conn.in_waiting)
        print(f"Raw scanap data length: {len(data)} bytes")
        text_data = data.decode('utf-8', errors='ignore')
        print(f"ScanAP as text (first 300 chars): {repr(text_data[:300])}")
        
        # Look for network information
        if "SSID" in text_data or "BSSID" in text_data or "channel" in text_data.lower():
            print("Found network-like information in response!")
        else:
            print("No obvious network information found")
    
    flipper.disconnect()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG to see more
    test_detailed_communication()
