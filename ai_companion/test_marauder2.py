#!/usr/bin/env python3
"""
Test script to figure out how to properly launch and communicate with Marauder
"""

import serial
import time
import sys
import os

# Add the ai_companion directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from serial_comm import FlipperSerial

def test_marauder_launch():
    """Test different ways to launch Marauder"""
    print("Testing Marauder launch procedures...")
    
    flipper = FlipperSerial('/dev/tty.usbmodemflip_Korgisap1')
    if not flipper.connect():
        print("Failed to connect")
        return
    
    flipper.start_reading()
    time.sleep(0.5)
    
    # Clear buffers
    flipper.serial_conn.reset_input_buffer()
    flipper.serial_conn.reset_output_buffer()
    
    # Let's see the initial state
    print("\n=== Initial state ===")
    flipper.send_command("")
    time.sleep(0.5)
    response = flipper.read_response(timeout=2)
    print(f"Initial: {repr(response)}")
    
    # Try different approaches to get to Marauder
    approaches = [
        ("Direct marauder command", lambda: flipper.send_command("marauder")),
        ("With newline", lambda: flipper.send_command("marauder\n")),
        ("Using run command", lambda: flipper.send_command("run marauder")),
        ("Using app launch", lambda: flipper.send_command("app marauder")),
    ]
    
    for name, approach_func in approaches:
        print(f"\n=== {name} ===")
        # Clear buffers before each attempt
        flipper.serial_conn.reset_input_buffer()
        flipper.serial_conn.reset_output_buffer()
        time.sleep(0.2)
        
        approach_func()
        time.sleep(2)  # Wait for app to load
        
        # Try to read any response
        response = flipper.read_response(timeout=3)
        print(f"Response after {name}: {repr(response)}")
        
        # Now try a simple marauder command to see if we're in the right place
        flipper.send_command("version")
        time.sleep(1)
        version_response = flipper.read_response(timeout=3)
        print(f"Version response: {repr(version_response)}")
        
        # If we got something that doesn't look like the ASCII art, we might be in marauder
        if version_response and not version_response.startswith('_.-------'):
            print(f"SUCCESS: Appears to be in Marauder app with {name}")
            break
    
    flipper.disconnect()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    test_marauder_launch()
