"""
Main Entry Point for Tapo Control and Battery Monitoring
Unified interface for Tapo P110 device control and laptop battery monitoring
"""

import asyncio
import sys
from dotenv import load_dotenv

from tapo_control import TapoP110Controller
from laptop_battery_loop import (
    get_battery_percent,
    is_plugged_in,
    monitor_battery_loop
)

# Load environment variables
load_dotenv()


async def show_device_info():
    """
    Display Tapo P110 device information
    """
    try:
        controller = TapoP110Controller()
        await controller.get_device_info()
        status = await controller.get_device_status()
        print(f"\nCurrent device status: {status}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def show_battery_status():
    """
    Display current laptop battery status
    """
    battery_percent = get_battery_percent()
    plugged_in = is_plugged_in()
    
    if battery_percent is None:
        print("ERROR: Unable to access battery information.")
        print("This script requires a laptop with battery monitoring capabilities.")
        return
    
    print("\nBattery Status:")
    print(f"  Battery level: {battery_percent:.1f}%")
    print(f"  Power status: {'Plugged in' if plugged_in else 'On battery'}")


async def control_device(action: str):
    """
    Control Tapo P110 device (turn on or off)
    
    Args:
        action: 'on' or 'off'
    """
    try:
        controller = TapoP110Controller()
        if action.lower() == 'on':
            await controller.turn_on()
        elif action.lower() == 'off':
            await controller.turn_off()
        else:
            print(f"Invalid action: {action}. Use 'on' or 'off'")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def start_battery_monitoring():
    """
    Start the battery monitoring loop
    """
    battery_percent = get_battery_percent()
    if battery_percent is None:
        print("ERROR: Unable to access battery information.")
        print("This script requires a laptop with battery monitoring capabilities.")
        return
    
    await monitor_battery_loop()


def print_menu():
    """
    Print the main menu options
    """
    print("\n" + "=" * 60)
    print("Tapo Control & Battery Monitoring")
    print("=" * 60)
    print("\nOptions:")
    print("  1. Show device info")
    print("  2. Show battery status")
    print("  3. Turn device ON")
    print("  4. Turn device OFF")
    print("  5. Start battery monitoring loop")
    print("  6. Exit")
    print()


async def interactive_menu():
    """
    Interactive menu for controlling Tapo device and battery monitoring
    """
    while True:
        print_menu()
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                await show_device_info()
            elif choice == '2':
                await show_battery_status()
            elif choice == '3':
                await control_device('on')
            elif choice == '4':
                await control_device('off')
            elif choice == '5':
                await start_battery_monitoring()
                break  # Exit menu after starting monitoring loop
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number between 1-6.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """
    Main entry point - supports command line arguments or interactive menu
    """
    # Check for command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'device-info':
            await show_device_info()
        elif command == 'battery-status':
            await show_battery_status()
        elif command == 'on':
            await control_device('on')
        elif command == 'off':
            await control_device('off')
        elif command == 'monitor' or command == 'loop':
            await start_battery_monitoring()
        elif command == 'help':
            print("\nUsage: python main.py [command]")
            print("\nCommands:")
            print("  device-info    - Show Tapo P110 device information")
            print("  battery-status - Show laptop battery status")
            print("  on             - Turn Tapo P110 device ON")
            print("  off            - Turn Tapo P110 device OFF")
            print("  monitor        - Start battery monitoring loop")
            print("  loop           - Alias for monitor")
            print("  help           - Show this help message")
            print("\nIf no command is provided, an interactive menu will be shown.")
        else:
            print(f"Unknown command: {command}")
            print("Use 'python main.py help' for usage information.")
    else:
        # No arguments - show interactive menu
        await interactive_menu()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()

