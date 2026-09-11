# Building and Installing WiFi Marauder on Flipper Zero

## Current Status
- Flipper Zero is connected via serial at `/dev/tty.usbmodemflip_Korgisap1`
- Basic communication works (can send commands, get responses)
- WiFi Marauder source code is present but **not yet built**
- Need to build the `.fap` file and install it on the Flipper Zero

## Build Requirements
Based on the source structure, this appears to be a Flipper Zero application that needs to be built with the Flipper Zero toolchain.

### Required Tools
1. **Flipper Zero SDK/toolchain** (fbt - Flipper Build Tool)
2. **CMake** (likely required)
3. **ARM GCC toolchain** for ESP32

## Build Process
Since there's no obvious build system (no CMakeLists.txt, Makefile), we need to:

1. **Install Flipper Zero development tools**:
   ```bash
   # Install fbt (Flipper Build Tool)
   # This typically comes with the Flipper Zero SDK
   ```

2. **Build the application**:
   The standard way to build Flipper Zero apps is:
   ```bash
   fbt build esp32_wifi_marauder
   ```
   or
   ```bash
   fbt build
   ```

3. **Install to Flipper Zero**:
   Once built, the `.fap` file needs to be installed:
   ```bash
   fbt install esp32_wifi_marauder
   ```
   Or via serial flash if the device supports it.

## Alternative Approach
If the Flipper Zero SDK/fbt is not available, we can:

1. **Use Docker** with the official Flipper Zero build environment
2. **Manual compilation** using the ARM GCC toolchain
3. **Pre-built binaries** if available from the Marauder repository

## Next Steps for AI Companion
Once the Marauder app is built and installed:

1. **Launch the app** via serial:
   ```
   app run esp32_wifi_marauder
   ```
   OR navigate through the menu: GPIO → In-Development → esp32_wifi_marauder

2. **Establish communication** with the AI companion:
   - Send commands to perform WiFi attacks
   - Receive reports and data back
   - Parse the marauder prompt (`:>` or similar)

3. **Implement AI control** in `ai_companion/marauder_controller.py`:
   - Command sending functions
   - Response parsing
   - Attack automation workflows
   - Report generation and analysis

## Immediate Actions
1. **Check if fbt is available** in a different location or install it
2. **Look for build instructions** in the documentation or README
3. **Try to build with generic Flipper Zero tools**
4. **If building fails, seek pre-built .fap file** from Marauder releases

## Serial Communication Notes
- Baud rate: 115200
- Line endings: `\r\n` (CR+LF)
- Prompt format: Normally `> ` for Flipper OS, likely `:> ` or similar for Marauder
- Commands are executed immediately upon receiving newline

