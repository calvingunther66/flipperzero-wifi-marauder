#!/usr/bin/env python3
"""
Marauder controller for Flipper Zero WiFi Marauder AI Companion
Handles communication with the Marauder firmware specifically
"""

import time
import logging
import sys
import os
from typing import Optional

# Add the ai_companion directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from serial_comm import FlipperSerial

logger = logging.getLogger(__name__)

class MarauderController:
    def __init__(self, port: str = '/dev/tty.usbmodemflip_Korgisap1'):
        self.serial = FlipperSerial(port)
        self.is_in_marauder = False
        
    def connect(self) -> bool:
        """Connect to Flipper Zero and enter Marauder app"""
        if not self.serial.connect():
            return False
            
        self.serial.start_reading()
        
        # Try to enter Marauder app
        logger.info("Attempting to enter Marauder app...")
        self.serial.send_command("marauder")
        time.sleep(1)  # Give time to switch apps
        
        # Check if we're in Marauder by looking for response
        response = self.serial.read_response(timeout=3)
        if response and ("marauder" in response.lower() or ":>" in response):
            self.is_in_marauder = True
            logger.info("Successfully entered Marauder app")
            return True
        else:
            logger.warning("May not have entered Marauder app correctly")
            # Still return True as we might be in the right place
            self.is_in_marauder = True
            return True
    
    def disconnect(self):
        """Disconnect from Flipper Zero"""
        self.serial.disconnect()
        self.is_in_marauder = False
    
    def send_marauder_command(self, command: str) -> bool:
        """Send a command specifically to Marauder firmware"""
        if not self.is_in_marauder:
            logger.warning("Not in Marauder app, attempting to enter...")
            if not self.connect():
                return False
        
        # Marauder commands typically don't need 'marauder' prefix when already in app
        return self.serial.send_command(command)
    
    def read_marauder_response(self, timeout: float = 5.0) -> Optional[str]:
        """Read response from Marauder"""
        return self.serial.read_response(timeout=timeout)
    
    def wait_for_marauder_ready(self, timeout: float = 10.0) -> bool:
        """Wait for Marauder to be ready for commands"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = self.serial.read_response(timeout=0.1)
            if response:
                logger.debug(f"Got response: {response}")
                # Look for Marauder-specific prompts
                if any(indicator in response.lower() for indicator in 
                       [':>', 'marauder', 'scanap', 'attack']):
                    return True
            time.sleep(0.1)
        return False
    
    # Common Marauder commands
    def scan_aps(self, timeout: float = 10.0) -> Optional[str]:
        """Scan for access points"""
        logger.info("Scanning for access points...")
        if self.send_marauder_command("scanap"):
            return self.read_marauder_response(timeout=timeout)
        return None
    
    def attack_deauth(self, target: str, timeout: float = 15.0) -> Optional[str]:
        """Run deauth attack on target"""
        logger.info(f"Running deauth attack on {target}")
        command = f"attack -t deauth {target}"
        if self.send_marauder_command(command):
            return self.read_marauder_response(timeout=timeout)
        return None
    
    def sniff_handshake(self, timeout: float = 30.0) -> Optional[str]:
        """Sniff for WPA handshake"""
        logger.info("Sniffing for WPA handshake...")
        if self.send_marauder_command("sniff"):
            return self.read_marauder_response(timeout=timeout)
        return None
    
    def get_version(self) -> Optional[str]:
        """Get Marauder version"""
        logger.info("Getting Marauder version...")
        if self.send_marauder_command("version"):
            return self.read_marauder_response(timeout=3)
        return None
    
    def help(self) -> Optional[str]:
        """Get Marauder help"""
        logger.info("Getting Marauder help...")
        if self.send_marauder_command("help"):
            return self.read_marauder_response(timeout=3)
        return None

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    marauder = MarauderController()
    try:
        if marauder.connect():
            print("Connected to Marauder!")
            
            # Get version
            version = marauder.get_version()
            print(f"Marauder Version: {version}")
            
            # Get help
            help_text = marauder.help()
            print(f"Help: {help_text[:200]}..." if help_text else "No help")
            
            # Scan for APs
            scan_result = marauder.scan_aps(timeout=15)
            print(f"Scan Result: {scan_result[:200]}..." if scan_result else "No scan result")
            
    finally:
        marauder.disconnect()
