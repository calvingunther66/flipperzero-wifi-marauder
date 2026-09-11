#!/usr/bin/env python3
"""
Test to see actual Marauder responses by capturing all data
"""

import serial
import time
import sys
import os
import threading

# Add the ai_companion directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from serial_comm import FlipperSerial

def test_with_full_capture():
    """Test by capturing all data that comes in"""
    print("Testing with full data capture...")
    
    flipper = FlipperSerial('/dev/tty.usbmodemflip_Korgisap1')
    if not flipper.connect():
        print("Failed to connect")
        return
    
    # We'll collect all data in a list
    all_data = []
    data_lock = threading.Lock()
    
    def data_callback(data):
        with data_lock:
            all_data.append(data)
        print(f"[CALLBACK] Received: {repr(data)}")
    
    flipper.set_response_callback(data_callback)
    flipper.start_reading()
    time.sleep(0.5)
    
    # Clear buffers
    flipper.serial_conn.reset_input_buffer()
    flipper.serial_conn.reset_output_buffer()
    
    # Enter Marauder
    print("\n=== Entering Marauder ===")
    flipper.send_command("marauder")
    time.sleep(2)
    
    # Try version
    print("\n=== Trying version ===")
    flipper.serial_conn.reset_input_buffer()
    flipper.send_command("version\n")
    time.sleep(3)
    
    # Check what we captured
    with data_lock:
        print(f"\nTotal data chunks received: {len(all_data)}")
        for i, data in enumerate(all_data):
            print(f"  {i}: {repr(data)}")
    
    # Clear callback data and try help
    all_data.clear()
    print("\n=== Trying help ===")
    flipper.serial_conn.reset_input_buffer()
    flipper.send_command("help\n")
    time.sleep(3)
    
    with data_lock:
        print(f"\nTotal data chunks received: {len(all_data)}")
        for i, data in enumerate(all_data):
            print(f"  {i}: {repr(data)}")
    
    # Try scanap
    all_data.clear()
    print("\n=== Trying scanap ===")
    flipper.serial_conn.reset_input_buffer()
    flipper.send_command("scanap\n")
    time.sleep(8)  # Longer for scan
    
    with data_lock:
        print(f"\nTotal data chunks received: {len(all_data)}")
        for i, data in enumerate(all_data):
            print(f"  {i}: {repr(data[:100])}{'...' if len(data) > 100 else ''}")
    
    flipper.disconnect()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    test_with_full_capture()
