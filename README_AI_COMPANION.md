# Flipper Zero WiFi Marauder AI Companion

This system integrates OpenRouter-based language AI with the Flipper Zero WiFi Marauder application to enable natural language control of wireless security assessments.

## Overview

The AI Companion allows you to control your Flipper Zero running WiFi Marauder using natural language commands. Instead of memorizing complex command syntax, you can simply say:

- "Scan for nearby WiFi networks"
- "Attempt to capture a WPA handshake from the strongest network"  
- "Perform a deauthentication attack on a specific target"
- "Start wardriving to collect WiFi geolocation data"
- "Set up an evil portal attack"

## Features

- 🤖 **Natural Language Interface**: Control Marauder using everyday English
- 🔍 **Intelligent Command Translation**: AI converts your requests into specific Marauder commands
- ⚠️ **Safety Awareness**: Gets confirmation for potentially disruptive attacks
- 📊 **Result Interpretation**: Explains what happened and suggests next steps
- 📡 **Full Marauder Support**: Access to all scanning, attack, and reconnaissance features
- 🔧 **Easy Setup**: Works with existing serial connection to Flipper Zero

## Components

1. **`openrouter_ai.py`** - Main AI controller with OpenRouter integration
2. **`serial_comm.py`** - Low-level serial communication with Flipper Zero  
3. **`marauder_controller.py`** - High-level Marauder command interface
4. **Various test scripts** - For development and verification

## Installation & Setup

### Prerequisites

1. **Flipper Zero** with WiFi Marauder installed (`.fap` file)
2. **Serial Connection** - Flipper Zero connected via USB/UART
3. **OpenRouter API Key** - Required for AI features

### Step-by-Step Setup

1. **Build & Install WiFi Marauder** (if not already done):
   ```bash
   # In the flipperzero-wifi-marauder directory
   ufbt build
   ufbt launch  # This installs and launches the app
   ```

2. **Get OpenRouter API Key**:
   - Visit https://openrouter.ai and sign up
   - Create an API key from your account settings
   - Copy the key (starts with `sk-or-v1-...`)

3. **Set Environment Variable**:
   ```bash
   export OPENROUTER_APIKEY="your-actual-openrouter-key-here"
   ```
   Add this to your `~/.zshrc` or `~/.bashrc` for permanent setup.

4. **Verify Serial Connection**:
   ```bash
   python3 ai_companion/serial_comm.py
   ```
   Should show successful connection and basic communication.

## Usage

### Interactive Mode (Recommended)

```bash
python3 ai_companion/openrouter_ai.py --interactive
```

Examples of what you can ask:
- `Scan for nearby WiFi networks`
- `Show me the current status and logs`  
- `Perform Bluetooth LE reconnaissance`
- `Attempt to capture WPA handshake from strongest network`
- `Start wardriving to collect WiFi data`
- `Set up an evil portal attack`
- `Perform a deauthentication attack`
- `Try a rickroll attack for fun`

### Single Command Mode

```bash
python3 ai_companion/openrouter_ai.py --command "Scan for nearby WiFi networks"
```

### Direct Serial Control (Without AI)

For testing or manual control:
```bash
python3 ai_companion/marauder_controller.py
```
This provides a simple interface to send Marauder commands directly.

## How It Works

1. **Natural Language Input** → You type a request in plain English
2. **AI Analysis** → OpenRouter AI analyzes your request and determines:
   - What type of operation (scan, attack, recon, etc.)
   - Specific Marauder commands needed
   - Safety considerations and estimated duration
3. **Command Execution** → The system sends the determined commands to your Flipper Zero via serial
4. **Result Collection** → Output from Marauder is captured and returned
5. **AI Summary** → AI explains what happened, results, and suggests next steps

## Safety Features

- **Confirmation Prompts**: For potentially disruptive attacks (deauth, evil portal, etc.)
- **Command Validation**: Checks if commands are valid before sending
- **Timeout Protection**: Prevents hanging on unresponsive commands
- **Error Handling**: Graceful handling of communication failures

## Marauder Commands Available

The AI has knowledge of these Marauder command categories:

### Scanning
- `scanall` - Scan all WiFi channels
- `pingscan` - Find active devices via ping
- `arpscan` - Find devices via ARP requests

### Reconnaissance  
- `recon wifi` - WiFi network reconnaissance
- `recon ble` - Bluetooth LE reconnaissance
- `recon status` - Show current system status
- `recon stop` - Stop ongoing operations

### Attacks
- `attack -t deauth` - Deauthentication attack
- `attack -t probe` - Probe request flood
- `attack -t rickroll` - Rickroll attack (play Rick Astley)
- `attack -t funny` - Funny SSID names
- `attack -t badmsg` - Bad message attacks
- `attack -t sleep` - Sleep deprivation attack
- `attack -t sae` - SAE flood (WPA3 attack)
- `attack -t csa` - Channel Switch Announcement
- `attack -t quiet` - Quiet attack mode

### Bluetooth Attacks
- `blespam -t sourapple` - Spoof as Apple device
- `blespam -t applejuice` - Attack Apple Bluetooth
- `blespam -t windows` - Windows Bluetooth spam
- `blespam -t samsung` - Samsung Bluetooth spam
- `blespam -t google` - Google Bluetooth spam
- `blespam -t flipper` - Flipper Bluetooth spam
- `blespam -t all` - Bluetooth spam all devices

### Special Functions
- `wardrive` - Collect WiFi data while moving
- `evilportal -c start` - Start evil portal attack
- `evilportal -c sethtml` - Set custom HTML for portal
- `sniffbeacon` - Sniff WiFi beacon frames
- `sniffpmkid` - Sniff for PMKID (WPA cracking)
- `sniffdeauth` - Sniff deauthentication frames

## Example Workflows

### Security Assessment
1. "Scan for nearby WiFi networks" → Discover targets
2. "Perform reconnaissance on the strongest network" → Gather details  
3. "Attempt to capture WPA handshake from target" → Get password hash
4. "Show me what we've captured" → Review results

### Bluetooth Testing
1. "Perform Bluetooth LE reconnaissance" → Find BT devices
2. "Try Bluetooth spoofing attack on Apple devices" → Test pairing
3. "Collect any captured Bluetooth data" → Review results

### Learning & Fun
1. "Perform a rickroll attack" → See the fun side of wireless
2. "Try the funny SSID attack" → Make people laugh
3. "Show me what attacks are available" → Learn the tool

## Troubleshooting

### Connection Issues
- **Problem**: "Failed to establish serial connection"
  - **Solution**: Check USB cable, ensure Flipper Zero is powered on, verify correct port

- **Problem**: "Command timeout" or no response
  - **Solution**: Make sure Marauder app is running (`loader open "/ext/apps/GPIO/esp32_wifi_marauder.fap"`)

### AI Issues
- **Problem**: "401 Unauthorized" from OpenRouter
  - **Solution**: Verify your API key is correct and has sufficient credits

- **Problem**: AI gives strange commands
  - **Solution**: The system includes safety checks - always review proposed commands before confirming

### Marauder-Specific
- **Problem**: Commands not found or not working
  - **Solution**: Ensure you have the latest WiFi Marauder build installed
  - **Solution**: Some commands require specific hardware capabilities

## Files Created

- `ai_companion/openrouter_ai.py` - Main AI controller
- `ai_companion/serial_comm.py` - Serial communication layer
- `ai_companion/marauder_controller.py` - Marauder command interface
- `ai_companion/*.py` - Various test and utility scripts
- `README_AI_COMPANION.md` - This documentation

## Next Steps / Enhancements

Planned improvements:
- [ ] Voice command integration (speech-to-text)
- [ ] GUI interface with visual network maps
- [ ] Automatic report generation after assessments
- [ ] Machine learning for attack optimization
- [ ] Integration with other security tools (aircrack-ng, etc.)
- [ ] Scheduled automated scanning/wardriving
- [ ] Enhanced AI with custom fine-tuning on Marauder commands

## Security & Ethical Use

⚠️ **IMPORTANT**: This tool is for authorized security testing only. 
- Only use on networks and devices you own or have explicit permission to test
- Respect privacy and local laws regarding wireless security testing
- The AI assistant will prompt for confirmation on potentially disruptive actions
- Always use responsibly and ethically

## License

This project is open source and available for modification and redistribution.

## Acknowledgments

- Flipper Zero team for the amazing hardware
- WiFi Marauder developers for the powerful firmware
- OpenRouter for providing access to advanced AI models
- The wireless security community for ongoing research and tools

---

**Happy hacking!** 🚀
