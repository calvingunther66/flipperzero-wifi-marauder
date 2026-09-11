#!/usr/bin/env python3
"""
Serial communication module for Flipper Zero WiFi Marauder AI Companion
"""

import serial
import time
import threading
import queue
from typing import Optional, Callable
import logging

logger = logging.getLogger(__name__)

class FlipperSerial:
    def __init__(self, port: str = '/dev/tty.usbmodemflip_Korgisap1', baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn: Optional[serial.Serial] = None
        self.read_queue = queue.Queue()
        self.running = False
        self.read_thread: Optional[threading.Thread] = None
        self.response_callback: Optional[Callable[[str], None]] = None
        
    def connect(self) -> bool:
        """Establish serial connection to Flipper Zero"""
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            # Clear buffers
            self.serial_conn.reset_input_buffer()
            self.serial_conn.reset_output_buffer()
            time.sleep(0.1)
            logger.info(f"Connected to Flipper Zero on {self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Flipper Zero: {e}")
            return False
    
    def disconnect(self):
        """Close serial connection"""
        self.running = False
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.join(timeout=2)
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        logger.info("Disconnected from Flipper Zero")
    
    def start_reading(self):
        """Start background thread for reading serial data"""
        if not self.serial_conn:
            raise RuntimeError("Not connected to Flipper Zero")
            
        self.running = True
        self.read_thread = threading.Thread(target=self._read_loop, daemon=True)
        self.read_thread.start()
        logger.info("Started serial reading thread")
    
    def _read_loop(self):
        """Background thread to read data from serial port"""
        buffer = ""
        while self.running and self.serial_conn and self.serial_conn.is_open:
            try:
                if self.serial_conn.in_waiting > 0:
                    data = self.serial_conn.read(self.serial_conn.in_waiting)
                    if data:
                        text = data.decode('utf-8', errors='ignore')
                        buffer += text
                        
                        # Process complete lines (Flipper uses newline termination)
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            line = line.strip()
                            if line:
                                self.read_queue.put(line)
                                if self.response_callback:
                                    self.response_callback(line)
                                
                time.sleep(0.01)  # Small delay to prevent CPU hogging
            except Exception as e:
                logger.error(f"Error in read loop: {e}")
                break
    
    def send_command(self, command: str) -> bool:
        """Send a command to Flipper Zero"""
        if not self.serial_conn or not self.serial_conn.is_open:
            logger.error("Serial connection not available")
            return False
            
        try:
            # Ensure command ends with newline
            if not command.endswith('\n'):
                command += '\n'
            self.serial_conn.write(command.encode('utf-8'))
            self.serial_conn.flush()
            logger.debug(f"Sent command: {command.strip()}")
            return True
        except Exception as e:
            logger.error(f"Failed to send command: {e}")
            return False
    
    def read_response(self, timeout: float = 5.0) -> Optional[str]:
        """Read a response from the queue with timeout"""
        try:
            return self.read_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def set_response_callback(self, callback: Callable[[str], None]):
        """Set callback for when response data is received"""
        self.response_callback = callback
    
    def wait_for_prompt(self, timeout: float = 10.0) -> bool:
        """Wait for Flipper to be ready for commands"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.read_queue.empty():
                response = self.read_queue.get()
                # Look for Flipper CLI prompt or Maraude-specific indicators
                if '>:' in response or 'marauder' in response.lower():
                    return True
            time.sleep(0.1)
        return False

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    flipper = FlipperSerial()
    if flipper.connect():
        flipper.start_reading()
        
        # Wait for Flipper to be ready
        if flipper.wait_for_prompt():
            print("Flipper is ready!")
            
            # Test sending a command
            flipper.send_command("help")
            response = flipper.read_response(timeout=3)
            print(f"Response: {response}")
        
        flipper.disconnect()
