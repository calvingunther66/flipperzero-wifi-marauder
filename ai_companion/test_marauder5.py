#!/usr/bin/env python3
"""
Test to see if we need to wait for the prompt differently
"""

import serial
import time
import sys
import os

# Add the ai_companion directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from serial_comm import FlipperSerial

def test_wait_for_prompt():
    """Test waiting for the marauder prompt"""
    print("Testing waiting for Marauder prompt...")
    
    flipper = FlipperSerial('/dev/tty.usbmodemflip_Korgisap1')
    if not flipper.connect():
        print("Failed to connect")
        return
    
    flipper.start_reading()
    time.sleep(0.5)
    
    # Clear buffers
    flipper.serial_conn.reset_input_buffer()
    flipper.serial_conn.reset_output_buffer()
    
    # Send marauder command
    print("Sending 'marauder' command...")
    flipper.send_command("marauder")
    
    # Wait and collect data for a few seconds
    start_time = time.time()
    all_data = []
    
    while time.time() - start_time < 5:  # Wait 5 seconds
        if flipper.serial_conn.in_waiting > 0:
            data = flipper.serial_conn.read(flipper.serial_conn.in_waiting)
            if data:
                text = data.decode('utf-8', errors='ignore')
                all_data.append(text)
                print(f"Received: {repr(text)}")
        time.sleep(0.1)
    
    print(f"\nTotal received: {len(all_data)} chunks")
    full_text = ''.join(all_data)
    print(f"Full text: {repr(full_text)}")
    
    # Now let's see if we're at a prompt by sending a newline and seeing what we get
    print("\n=== Sending newline to check for prompt ===")
    flipper.serial_conn.reset_input_buffer()
    flipper.send_command("\n")
    time.sleep(1)
    
    if flipper.serial_conn.in_waiting > 0:
        data = flipper.serial_conn.read(flipper.serial_conn.in_waiting)
        if data:
            text = data.decode('utf-8', errors='ignore')
            print(f"Response to newline: {repr(text)}")
            
            # Check if this looks like a prompt
            if ':>' in text or 'marauder' in text.lower():
                print("Looks like we got a prompt!")
                
                # Now try a real command
                print("\n=== Trying version command ===")
                flipper.serial_conn.reset_input_buffer()
                flipper.send_command("version\n")
                time.sleep(2)
                
                if flipper.serial_conn.in_waiting > 0:
                    data = flipper.serial_conn.read(flipper.serial_conn.in_waiting)
                    if data:
                        text = data.decode('utf-8', errors='ignore')
                        print(f"Version response: {repr(text)}")
    else:
        print("No response to newline")
    
    flipper.disconnect()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    test_wait_for_prompt()
