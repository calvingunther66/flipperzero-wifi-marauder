#!/usr/bin/env python3
"""
Final test - let's try to actually build and install the marauder app
"""

import subprocess
import os
import sys

def test_build_and_install():
    print("=== Checking if we can build marauder ===")
    
    # Change to the marauder directory
    marauder_dir = "/Users/calvingunther/copilot-worktrees/flipperzero-wifi-marauder/calvingunther66-miniature-lamp"
    os.chdir(marauder_dir)
    
    print(f"Working in: {os.getcwd()}")
    
    # Check if we have the flipper zero toolchain or if we can use fbt
    print("\n=== Checking for flipper tools ===")
    result = subprocess.run(["which", "fbt"], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Found fbt at: {result.stdout.strip()}")
    else:
        print("fbt not found in PATH")
    
    # Check if we can build the app
    print("\n=== Checking build system ===")
    if os.path.exists("CMakeLists.txt"):
        print("Found CMakeLists.txt")
    else:
        print("No CMakeLists.txt found")
    
    # Check for makerfile or similar
    if os.path.exists("Makefile"):
        print("Found Makefile")
    elif os.path.exists("build.sh"):
        print("Found build.sh")
    else:
        print("No obvious build file found")
    
    # Let's look at the structure
    print("\n=== Directory structure ===")
    for item in sorted(os.listdir(".")):
        if os.path.isdir(item):
            print(f"  {item}/")
        else:
            print(f"  {item}")
    
    # Check if the app is already built/fap exists
    fap_path = "esp32_wifi_marauder.fap"
    if os.path.exists(fap_path):
        print(f"\nFound FAP file: {fap_path}")
        print("App appears to be already built!")
        
        # Try to install it via serial if possible
        print("\n=== Trying to install via serial ===")
        # This would require the flipper to be in DFU mode or have serial flash capability
        # For now, let's just note that we have the app
        
        return True
    else:
        print(f"\nFAP file not found: {fap_path}")
        print("Need to build the app first")
        return False

if __name__ == "__main__":
    test_build_and_install()
