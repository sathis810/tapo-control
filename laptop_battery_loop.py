"""
Laptop Battery Monitoring and Charging Control Script
Monitors laptop battery level and controls charging via Tapo P110 smart plug
Charging thresholds: Start at 40%, Stop at 80%
"""

import os
import asyncio
import time
from datetime import datetime
from dotenv import load_dotenv
import psutil

from tapo_control import TapoP110Controller

# Load environment variables
load_dotenv()


def get_battery_percent():
    """
    Get the current battery percentage
    
    Returns:
        Battery percentage (0-100) or None if battery info is not available
    """
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return None
        return battery.percent
    except Exception as e:
        print(f"Error getting battery level: {e}")
        return None


def is_plugged_in():
    """
    Check if the laptop is plugged into AC power
    
    Returns:
        True if plugged in, False if on battery, None if unable to determine
    """
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return None
        return battery.power_plugged
    except Exception as e:
        print(f"Error checking power status: {e}")
        return None


async def monitor_battery_loop(
    start_threshold: int = None,
    stop_threshold: int = None,
    check_interval: int = None
):
    """
    Main loop to monitor battery level and control charging
    
    Args:
        start_threshold: Battery percentage to start charging (default: from env or 40)
        stop_threshold: Battery percentage to stop charging (default: from env or 80)
        check_interval: Time in seconds between battery checks (default: from env or 60)
    """
    # Get thresholds from environment variables with defaults
    if start_threshold is None:
        start_threshold = int(os.getenv('BATTERY_START_THRESHOLD', '40'))
    if stop_threshold is None:
        stop_threshold = int(os.getenv('BATTERY_STOP_THRESHOLD', '80'))
    if check_interval is None:
        check_interval = int(os.getenv('BATTERY_CHECK_INTERVAL', '60'))
    print(f"Starting battery monitoring loop...")
    print(f"  Start charging threshold: {start_threshold}%")
    print(f"  Stop charging threshold: {stop_threshold}%")
    print(f"  Check interval: {check_interval} seconds")
    print(f"  Press Ctrl+C to stop\n")
    
    try:
        controller = TapoP110Controller()
        print("Successfully connected to Tapo P110 device\n")
    except Exception as e:
        print(f"Error initializing Tapo controller: {e}")
        print("Please ensure your .env file is configured correctly")
        return
    
    last_action = None
    
    while True:
        try:
            battery_percent = get_battery_percent()
            plugged_in = is_plugged_in()
            
            if battery_percent is None:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Unable to get battery information")
                await asyncio.sleep(check_interval)
                continue
            
            # Get current device status
            device_status = await controller.get_device_status()
            is_charger_on = (device_status == "ON")
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            power_status = "Plugged in" if plugged_in else "On battery"
            
            print(f"[{timestamp}] Battery: {battery_percent:.1f}% | {power_status} | Charger: {'ON' if is_charger_on else 'OFF'}")
            
            # Decision logic for charging control
            if battery_percent <= start_threshold:
                if not is_charger_on:
                    print(f"  → Battery at {battery_percent:.1f}% (≤ {start_threshold}%), turning charger ON")
                    result = await controller.turn_on()
                    if result:
                        last_action = "turned_on"
                        print(f"  ✓ Charger turned ON successfully")
                    else:
                        print(f"  ✗ Failed to turn charger ON")
                else:
                    if last_action != "already_on":
                        print(f"  → Battery at {battery_percent:.1f}% (≤ {start_threshold}%), charger already ON")
                        last_action = "already_on"
            
            elif battery_percent >= stop_threshold:
                if is_charger_on:
                    print(f"  → Battery at {battery_percent:.1f}% (≥ {stop_threshold}%), turning charger OFF")
                    result = await controller.turn_off()
                    if result:
                        last_action = "turned_off"
                        print(f"  ✓ Charger turned OFF successfully")
                    else:
                        print(f"  ✗ Failed to turn charger OFF")
                else:
                    if last_action != "already_off":
                        print(f"  → Battery at {battery_percent:.1f}% (≥ {stop_threshold}%), charger already OFF")
                        last_action = "already_off"
            
            else:
                # Battery is between thresholds
                if last_action not in ["in_range_on", "in_range_off"]:
                    status_msg = "ON" if is_charger_on else "OFF"
                    print(f"  → Battery at {battery_percent:.1f}% (between {start_threshold}% and {stop_threshold}%), charger remains {status_msg}")
                    last_action = "in_range_on" if is_charger_on else "in_range_off"
            
            print()  # Empty line for readability
            
            await asyncio.sleep(check_interval)
            
        except KeyboardInterrupt:
            print("\n\nStopping battery monitoring loop...")
            break
        except Exception as e:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error in monitoring loop: {e}")
            import traceback
            traceback.print_exc()
            print(f"Retrying in {check_interval} seconds...\n")
            await asyncio.sleep(check_interval)

