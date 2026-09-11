#!/usr/bin/env python3
"""
Listen to serial with detailed timing
"""

import serial
import time

def listen_detailed():
    port = '/dev/tty.usbmodemflip_Korgisap1'
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Listening on {port}...")
        start = time.time()
        last_data_time = start
        while time.time() - start < 10:  # Listen for 10 seconds
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if data:
                    text = data.decode('utf-8', errors='ignore')
                    timestamp = time.time()
                    print(f"[{timestamp-start:.3f}s] Received: {repr(text)}")
                    last_data_time = timestamp
            else:
                # Show periodic heartbeat if no data for 2 seconds
                if time.time() - last_data_time > 2:
                    print(f"[{time.time()-start:.3f}s] No data for 2+ seconds")
                    last_data_time = time.time()  # Reset to avoid spam
            time.sleep(0.05)  # Check more frequently
        print("\nDone listening.")
        ser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    listen_detailed()
