#!/usr/bin/env python3
"""
OpenRouter AI integration for controlling Flipper Zero WiFi Marauder
"""

import requests
import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import time

# Import our existing serial communication
from serial_comm import FlipperSerial as SerialConnection
from marauder_controller import MarauderController

class TaskType(Enum):
    SCAN = "scan"
    ATTACK = "attack"
    RECON = "recon"
    CONFIGURE = "configure"
    VIEW_LOGS = "view_logs"
    EXECUTE_SCRIPT = "execute_script"

@dataclass
class AttackCommand:
    command: str
    description: str
    expected_duration: int  # seconds
    requires_confirmation: bool = False

class OpenRouterAI:
    def __init__(self, api_key: str = None, serial_port: str = None):
        """
        Initialize the OpenRouter AI agent
        
        Args:
            api_key: OpenRouter API key (if None, will try to get from environment)
            serial_port: Serial port for Flipper Zero (if None, will auto-detect)
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key required. Set OPENROUTER_API_KEY environment variable or pass api_key parameter.")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/calvingunther66/flipperzero-wifi-marauder",
            "X-Title": "Flipper Zero WiFi Marauder AI Controller"
        }
        
        # Initialize serial connection and marauder controller
        self.serial_conn = SerialConnection(serial_port) if serial_port else SerialConnection()
        self.marauder = MarauderController(self.serial_conn)
        
        # Available marauder commands for reference
        self.available_commands = self._load_available_commands()
        
        # Conversation history for context
        self.conversation_history = [
            {
                "role": "system",
                "content": """You are an AI assistant controlling a Flipper Zero device running the WiFi Marauder application. 
                Your goal is to help users perform wireless security assessments and attacks using natural language commands.
                
                You have access to the following capabilities:
                - WiFi network scanning (scanall, pingscan, arpscan)
                - Reconnaissance (recon wifi, recon ble, recon status)
                - Various attacks (deauth, probe, rickroll, funny, badmsg, sleep, sae flood, csa, quiet, etc.)
                - Bluetooth attacks (blespam with various targets)
                - Evil portal attacks
                - Wardriving and logging
                - GPS functionality
                - Script execution
                
                When users give you high-level goals, break them down into specific Marauder commands.
                Always explain what you're doing and why.
                For potentially disruptive attacks, ask for confirmation before proceeding.
                Provide summaries of results after commands complete.
                
                Current Marauder application status: Connected and ready."""
            }
        ]
    
    def _load_available_commands(self) -> Dict[str, Any]:
        """Load available Marauder commands for AI reference"""
        return {
            "scan": {
                "scanall": "Scan all nearby WiFi networks",
                "pingscan": "Ping sweep to find active devices",
                "arpscan": "ARP scan to find devices on network"
            },
            "recon": {
                "wifi": "WiFi reconnaissance",
                "ble": "Bluetooth LE reconnaissance", 
                "status": "Show current status",
                "stop": "Stop ongoing operations"
            },
            "attack": {
                "deauth": "Deauthentication attack",
                "probe": "Probe request attack",
                "rickroll": "Rickroll attack (play Rick Astley on vulnerable devices)",
                "funny": "Funny SSID attack",
                "badmsg": "Bad message attack",
                "sleep": "Sleep deprivation attack",
                "sae flood": "SAE flood attack (WPA3)",
                "csa": "Channel Switch Announcement attack",
                "quiet": "Quiet attack",
                "sour apple": "Bluetooth Spoof to Apple devices",
                "apple juice": "Bluetooth attack on Apple devices",
                "swiftpair spam": "Bluetooth SwiftPair spam",
                "samsung spam": "Bluetooth Samsung spam",
                "google spam": "Bluetooth Google spam",
                "flipper spam": "Bluetooth Flipper spam",
                "bt spam all": "Bluetooth spam all devices"
            },
            "blespam": {
                "sourapple": "Spoof as Apple device",
                "applejuice": "Attack Apple devices",
                "windows": "Windows Bluetooth spam",
                "samsung": "Samsung Bluetooth spam",
                "google": "Google Bluetooth spam",
                "flipper": "Flipper Bluetooth spam",
                "all": "Bluetooth spam all"
            },
            "wardrive": {
                "": "Start wardriving (collect WiFi data while moving)"
            },
            "evilportal": {
                "start": "Start evil portal attack",
                "sethtml": "Set custom HTML for evil portal",
                "setap": "Set evil portal AP configuration"
            },
            "sniff": {
                "beacon": "Sniff beacon frames",
                "deauth": "Sniff deauthentication frames",
                "pmkid": "Sniff PMKID attempts (for WPA cracking)",
                "probe": "Sniff probe requests",
                "pwn": "Sniff for PWN attempts",
                "raw": "Sniff raw 802.11 frames",
                "bt": "Sniff Bluetooth traffic",
                "skim": "Sniff for credit card skimmers",
                "airtag": "Sniff for Apple AirTags",
                "flipper": "Sniff for Flipper Zero devices",
                "flock": "Sniff for Flock safety devices",
                "meta": "Sniff for Meta (Facebook) devices",
                "mactrack": "Sniff for MAC tracking",
                "packetcount": "Count packets",
                "multissid": "Sniff multi-SSID networks",
                "sae": "Sniff SAE exchanges"
            }
        }
    
    def chat_with_ai(self, user_message: str, model: str = "anthropic/claude-3.5-sonnet") -> str:
        """
        Send a message to OpenRouter AI and get response
        
        Args:
            user_message: User's input message
            model: AI model to use (default: Claude 3.5 Sonnet)
            
        Returns:
            AI response string
        """
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare the request
        payload = {
            "model": model,
            "messages": self.conversation_history,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            
            # Add AI response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
            
        except Exception as e:
            error_msg = f"Error communicating with OpenRouter AI: {str(e)}"
            print(error_msg)
            return error_msg
    
    def execute_marauder_command(self, command: str, description: str = "") -> Dict[str, Any]:
        """
        Execute a Marauder command and return results
        
        Args:
            command: The Marauder command to execute
            description: Human-readable description of what the command does
            
        Returns:
            Dictionary with success status, output, and metadata
        """
        print(f"Executing Marauder command: {command}")
        if description:
            print(f"Description: {description}")
        
        try:
            # Launch marauder app if not already running
            if not self.marauder.is_app_running():
                print("Launching Marauder application...")
                self.marauder.launch_app()
                time.sleep(2)  # Wait for app to start
            
            # Execute the command
            result = self.marauder.send_command(command)
            
            # Wait a bit for command to complete (adjust based on command type)
            time.sleep(1)
            
            # Get any additional output
            additional_output = self.marauder.get_output(timeout=2)
            if additional_output:
                result['output'] += additional_output
            
            return {
                "success": True,
                "command": command,
                "description": description,
                "output": result.get('output', ''),
                "error": result.get('error', ''),
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "success": False,
                "command": command,
                "description": description,
                "output": "",
                "error": str(e),
                "timestamp": time.time()
            }
    
    def process_user_request(self, user_input: str) -> str:
        """
        Process a user request and coordinate AI response with Marauder execution
        
        Args:
            user_input: User's natural language request
            
        Returns:
            Formatted response to user
        """
        # First, get AI analysis of what the user wants
        ai_analysis_prompt = f"""
        User request: "{user_input}"
        
        Analyze this request and determine:
        1. What type of operation is requested (scan, attack, recon, etc.)
        2. Specific Marauder commands that would fulfill this request
        3. Any safety considerations or confirmations needed
        4. Expected duration and outcomes
        
        Available Marauder commands include:
        - Scan: scanall, pingscan, arpscan
        - Recon: recon wifi, recon ble, recon status, recon stop
        - Attack: deauth, probe, rickroll, funny, badmsg, sleep, sae flood, csa, quiet, etc.
        - Bluetooth attacks: blespam -t sourapple, blespam -t applejuice, etc.
        - Wardrive: wardrive
        - Evil portal: evilportal -c start, evilportal -c sethtml, evilportal -c setap
        - Sniff: sniffbeacon, sniffdeauth, sniffpmkid, sniffprobe, etc.
        
        Provide your analysis in JSON format:
        {{
            "operation_type": "scan|attack|recon|configure|view_logs|execute_script",
            "commands": ["command1", "command2", ...],
            "description": "Human-readable description of what will be done",
            "safety_check": true/false (whether user confirmation is recommended),
            "estimated_duration": number_of_seconds,
            "explanation": "Explanation for the user about what you're doing and why"
        }}
        """
        
        ai_response = self.chat_with_ai(ai_analysis_prompt)
        
        # Try to parse JSON response
        try:
            # Extract JSON from AI response (might be wrapped in markdown or text)
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                # Fallback if AI doesn't return proper JSON
                analysis = {
                    "operation_type": "unknown",
                    "commands": [],
                    "description": "Could not parse AI response",
                    "safety_check": True,
                    "estimated_duration": 5,
                    "explanation": ai_response
                }
        except json.JSONDecodeError:
            analysis = {
                "operation_type": "unknown",
                "commands": [],
                "description": "Could not parse AI response",
                "safety_check": True,
                "estimated_duration": 5,
                "explanation": ai_response
            }
        
        # Show explanation to user
        print(f"\nAI Analysis: {analysis['explanation']}")
        
        # Ask for confirmation if safety check is recommended
        if analysis.get('safety_check', False) and analysis.get('commands'):
            print(f"\n⚠️  Safety Check Recommended")
            print(f"Planned commands: {', '.join(analysis['commands'])}")
            print(f"Estimated duration: {analysis.get('estimated_duration', 5)} seconds")
            
            user_confirm = input("\nProceed with these commands? (y/N): ").lower().strip()
            if user_confirm not in ['y', 'yes']:
                return "Operation cancelled by user."
        
        # Execute the commands
        results = []
        for command in analysis.get('commands', []):
            # Find description for this command
            desc = self._get_command_description(command)
            result = self.execute_marauder_command(command, desc)
            results.append(result)
            
            # Show immediate feedback
            if result['success']:
                print(f"✅ Command '{command}' executed successfully")
                if result['output'].strip():
                    print(f"   Output: {result['output'][:200]}{'...' if len(result['output']) > 200 else ''}")
            else:
                print(f"❌ Command '{command}' failed: {result['error']}")
        
        # Generate final summary
        summary_prompt = f"""
        User originally requested: "{user_input}"
        
        AI Analysis: {analysis['explanation']}
        
        Commands executed:
        {chr(10).join([f"- {r['command']}: {'SUCCESS' if r['success'] else 'FAILED'} ({r.get('description', '')})" for r in results])}
        
        Outputs:
        {chr(10).join([f"- {r['command']}: {r['output'][:100]}{'...' if len(r['output']) > 100 else ''}" for r in results if r['output']])}
        
        Errors:
        {chr(10).join([f"- {r['command']}: {r['error']}" for r in results if not r['success'] and r['error']])}
        
        Provide a comprehensive summary to the user explaining:
        1. What was requested
        2. What was done
        3. Results and findings
        4. Any recommendations for next steps
        5. Security considerations (if any attacks were performed)
        """
        
        final_response = self.chat_with_ai(summary_prompt)
        return final_response
    
    def _get_command_description(self, command: str) -> str:
        """Get human-readable description for a command"""
        # Check our command dictionary
        for category, subcommands in self.available_commands.items():
            if isinstance(subcommands, dict):
                if command in subcommands:
                    return subcommands[command]
                # Check for prefixed commands like "attack -t deauth"
                for subcmd, desc in subcommands.items():
                    if command.startswith(subcmd):
                        return desc
            elif category == command:  # Direct match like "wardrive" -> ""
                return subcommands if subcommands else "Execute wardriving"
        
        # Fallback descriptions
        if command.startswith("scan"):
            return "WiFi network scanning"
        elif command.startswith("recon"):
            return "Wireless reconnaissance"
        elif command.startswith("attack"):
            return "Wireless attack"
        elif command.startswith("blespam"):
            return "Bluetooth attack"
        elif command.startswith("evilportal"):
            return "Evil portal attack"
        elif command.startswith("sniff"):
            return "Packet sniffing"
        elif command == "wardrive":
            return "Wardriving (collect WiFi data)"
        elif command == "help":
            "Show help"
        else:
            return f"Execute Marauder command: {command}"
    
    def interactive_mode(self):
        """Run interactive mode for continuous user interaction"""
        print("🤖 Flipper Zero WiFi Marauder AI Companion")
        print("=" * 50)
        print("Commands:")
        print("  - Type natural language requests to control the Marauder")
        print("  - Examples:")
        print("    * 'Scan for nearby WiFi networks'")
        print("    * 'Attempt to capture WPA handshake from the strongest network'")
        print("    * 'Perform a deauthentication attack on a specific network'")
        print("    * 'Start wardriving to collect WiFi data'")
        print("    * 'Show me the current status and logs'")
        print("  - Type 'quit' or 'exit' to stop")
        print("  - Type 'help' for this help message")
        print()
        
        # Test connection
        print("Testing connection to Flipper Zero...")
        if self.serial_conn.connect():
            print("✅ Serial connection established")
        else:
            print("❌ Failed to establish serial connection")
            print("Please check that your Flipper Zero is connected and powered on")
            return
        
        print("\nReady to accept commands. What would you like to do?\n")
        
        while True:
            try:
                user_input = input("> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    print("\n🤖 Flipper Zero WiFi Marauder AI Companion")
                    print("=" * 50)
                    print("Examples of what you can ask:")
                    print("  🔍 Scan & Reconnaissance:")
                    print("    * 'Scan for nearby WiFi networks'")
                    print("    * 'Perform Bluetooth LE reconnaissance'")
                    print("    * 'Show current device status'")
                    print("  📡 Attacks:")
                    print("    * 'Perform a deauthentication attack'")
                    print("    * 'Try to capture WPA handshake'")
                    print("    * 'Execute a rickroll attack'")
                    print("    * 'Perform Bluetooth spoofing attacks'")
                    print("  🚗 Wardriving:")
                    print("    * 'Start wardriving to collect WiFi data'")
                    print("  👻 Evil Portal:")
                    print("    * 'Set up an evil portal attack'")
                    print("  📊 Analysis:")
                    print("    * 'Show me the captured logs'")
                    print("    * 'What networks have we discovered?'")
                    print()
                    continue
                
                if not user_input:
                    continue
                
                print("\n🤖 Processing your request...")
                response = self.process_user_request(user_input)
                print(f"\n🤖 AI Response:\n{response}\n")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'quit' to exit.\n")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.serial_conn.close()
        except:
            pass

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Flipper Zero WiFi Marauder AI Companion")
    parser.add_argument("--api-key", help="OpenRouter API key (can also use OPENROUTER_API_KEY env var)")
    parser.add_argument("--port", help="Serial port for Flipper Zero (auto-detect if not specified)")
    parser.add_argument("--model", default="anthropic/claude-3.5-sonnet", help="AI model to use")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--command", "-c", help="Single command to execute (non-interactive)")
    
    args = parser.parse_args()
    
    try:
        # Initialize AI companion
        ai = OpenRouterAI(api_key=args.api_key, serial_port=args.port)
        
        if args.interactive or not args.command:
            # Interactive mode
            ai.interactive_mode()
        else:
            # Single command mode
            print(f"Executing: {args.command}")
            response = ai.process_user_request(args.command)
            print(f"\nResponse:\n{response}")
        
        ai.cleanup()
        
    except Exception as e:
        print(f"❌ Failed to initialize AI companion: {str(e)}")
        print("\nMake sure:")
        print("1. Your Flipper Zero is connected via serial")
        print("2. You have set OPENROUTER_API_KEY environment variable or provided --api-key")
        print("3. The WiFi Marauder app is built and available")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
