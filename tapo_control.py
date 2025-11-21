"""
Tapo P110 Device Control Script
Controls Tapo P110 smart plugs via local network using Tapo API
"""

import os
import asyncio
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from tapo import ApiClient
from tapo.requests import EnergyDataInterval, PowerDataInterval

# Load environment variables
load_dotenv()


def get_quarter_start_month(today: datetime) -> int:
    """
    Calculate the starting month of the quarter for a given date
    
    Args:
        today: The datetime object to calculate the quarter start month for
        
    Returns:
        The month number (1-12) representing the first month of the quarter
    """
    return ((today.month - 1) // 3) * 3 + 1


class TapoP110Controller:
    """
    Controller class for Tapo P110 smart plug devices using local network API
    """
    
    def __init__(self, email: str = None, password: str = None, device_ip: str = None):
        """
        Initialize the Tapo P110 controller with credentials and device IP
        
        Args:
            email: Tapo account email (or from .env file)
            password: Tapo account password (or from .env file)
            device_ip: Device IP address (or from .env file)
        """
        self.email = email or os.getenv('TP_LINK_EMAIL')
        self.password = password or os.getenv('TP_LINK_PASSWORD')
        self.device_ip = device_ip or os.getenv('TAPO_DEVICE_IP')
        
        if not self.email or not self.password:
            raise ValueError("Email and password must be provided either as arguments or in .env file")
        
        if not self.device_ip:
            raise ValueError("Device IP address must be provided either as argument or in .env file as TAPO_DEVICE_IP")
        
        self.client = ApiClient(self.email, self.password)
        self.device = None
    
    async def _ensure_device_connected(self):
        """
        Ensure device is connected. Connect if not already connected.
        
        Returns:
            Device object if successful, None otherwise
        """
        if self.device is None:
            try:
                self.device = await self.client.p110(self.device_ip)
            except Exception as e:
                print(f"Error connecting to device at {self.device_ip}: {e}")
                import traceback
                traceback.print_exc()
                return None
        return self.device
    
    async def turn_on(self):
        """
        Turn on the P110 device
        
        Returns:
            True if successful, False otherwise
        """
        device = await self._ensure_device_connected()
        if not device:
            print("Device not found or could not connect")
            return False
        
        try:
            # Get current status before turning on
            try:
                device_info = await device.get_device_info()
                is_currently_on = device_info.device_on
                status_str = "ON" if is_currently_on else "OFF"
                print(f"Device current status: {status_str}")
            except Exception as e:
                print(f"Warning: Could not determine current status: {e}")
                print("  Proceeding with turn on command anyway...")
            
            # Turn on the device
            print(f"Executing turn on command...")
            try:
                await device.on()
                print(f"[OK] Command executed successfully")
            except Exception as cmd_error:
                print(f"[ERROR] Error executing turn on command: {cmd_error}")
                import traceback
                traceback.print_exc()
                return False
            
            # Wait a moment for the command to process
            await asyncio.sleep(1)
            
            # Verify the device is actually on
            try:
                device_info = await device.get_device_info()
                is_now_on = device_info.device_on
                
                if is_now_on:
                    print(f"[SUCCESS] Successfully turned ON device")
                    return True
                else:
                    print(f"[WARNING] Device status is still OFF")
                    print(f"  The turn on command may not have worked. Please check the device manually.")
                    return False
            except Exception as e:
                print(f"[INFO] Command executed, but could not verify device status: {e}")
                print(f"  Please check the physical device to confirm it turned on")
                return True  # Assume success if command executed without error
        except Exception as e:
            print(f"[ERROR] Error turning device on: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def turn_off(self):
        """
        Turn off the P110 device
        
        Returns:
            True if successful, False otherwise
        """
        device = await self._ensure_device_connected()
        if not device:
            print("Device not found or could not connect")
            return False
        
        try:
            # Get current status before turning off
            try:
                device_info = await device.get_device_info()
                is_currently_on = device_info.device_on
                status_str = "ON" if is_currently_on else "OFF"
                print(f"Device current status: {status_str}")
            except Exception as e:
                print(f"Warning: Could not determine current status: {e}")
                print("  Proceeding with turn off command anyway...")
            
            # Turn off the device
            print(f"Executing turn off command...")
            try:
                await device.off()
                print(f"[OK] Command executed successfully")
            except Exception as cmd_error:
                print(f"[ERROR] Error executing turn off command: {cmd_error}")
                import traceback
                traceback.print_exc()
                return False
            
            # Wait a moment for the command to process
            await asyncio.sleep(1)
            
            # Verify the device is actually off
            try:
                device_info = await device.get_device_info()
                is_now_on = device_info.device_on
                
                if not is_now_on:
                    print(f"[SUCCESS] Successfully turned OFF device")
                    return True
                else:
                    print(f"[WARNING] Device status is still ON")
                    print(f"  The turn off command may not have worked. Please check the device manually.")
                    return False
            except Exception as e:
                print(f"[INFO] Command executed, but could not verify device status: {e}")
                print(f"  Please check the physical device to confirm it turned off")
                return True  # Assume success if command executed without error
        except Exception as e:
            print(f"[ERROR] Error turning device off: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def get_device_info(self):
        """
        Get information about the P110 device
        
        Returns:
            Device info object if successful, None otherwise
        """
        device = await self._ensure_device_connected()
        if not device:
            print("Device not found or could not connect")
            return None
        
        try:
            device_info = await device.get_device_info()
            print(f"\nDevice Information:")
            print(f"  IP Address: {self.device_ip}")
            print(f"  Device On: {device_info.device_on}")
            print(f"  Device ID: {device_info.device_id}")
            print(f"  Model: {device_info.model}")
            print(f"  Hardware Version: {device_info.hw_ver}")
            print(f"  Firmware Version: {device_info.fw_ver}")
            print(f"  Type: {device_info.type}")
            if hasattr(device_info, 'nickname'):
                print(f"  Nickname: {device_info.nickname}")
            return device_info
        except Exception as e:
            print(f"Error retrieving device info: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_device_status(self):
        """
        Get the current power status of the device
        
        Returns:
            String status: "ON" or "OFF"
        """
        device = await self._ensure_device_connected()
        if not device:
            return None
        
        try:
            device_info = await device.get_device_info()
            return "ON" if device_info.device_on else "OFF"
        except Exception as e:
            print(f"Error getting device status: {e}")
            return None
    
    async def get_current_power(self):
        """
        Get current power consumption data from the P110 device
        
        Returns:
            Current power object if successful, None otherwise
        """
        device = await self._ensure_device_connected()
        if not device:
            print("Device not found or could not connect")
            return None
        
        try:
            current_power = await device.get_current_power()
            print(f"\nCurrent Power:")
            print(f"  {current_power.to_dict()}")
            return current_power
        except Exception as e:
            print(f"Error retrieving current power: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_device_usage(self):
        """
        Get device usage statistics from the P110 device
        
        Returns:
            Device usage object if successful, None otherwise
        """
        device = await self._ensure_device_connected()
        if not device:
            print("Device not found or could not connect")
            return None
        
        try:
            device_usage = await device.get_device_usage()
            print(f"\nDevice Usage:")
            print(f"  {device_usage.to_dict()}")
            return device_usage
        except Exception as e:
            print(f"Error retrieving device usage: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_energy_usage(self):
        """
        Get energy usage statistics from the P110 device
        
        Returns:
            Energy usage object if successful, None otherwise
        """
        device = await self._ensure_device_connected()
        if not device:
            print("Device not found or could not connect")
            return None
        
        try:
            energy_usage = await device.get_energy_usage()
            print(f"\nEnergy Usage:")
            print(f"  {energy_usage.to_dict()}")
            return energy_usage
        except Exception as e:
            print(f"Error retrieving energy usage: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_energy_data(self, interval: EnergyDataInterval, start_date: datetime = None):
        """
        Get energy data from the P110 device with specified interval
        
        Args:
            interval: EnergyDataInterval enum (Hourly, Daily, or Monthly)
            start_date: Start date for the data query. Defaults to current UTC time.
                       - For Hourly: inclusive interval, must not be greater than 8 days
                       - For Daily: must be the first day of a quarter
                       - For Monthly: must be the first day of a year
        
        Returns:
            Energy data object if successful, None otherwise
        """
        device = await self._ensure_device_connected()
        if not device:
            print("Device not found or could not connect")
            return None
        
        if start_date is None:
            start_date = datetime.now(timezone.utc)
        
        try:
            energy_data = await device.get_energy_data(interval, start_date)
            interval_name = interval.name if hasattr(interval, 'name') else str(interval)
            print(f"\nEnergy data ({interval_name.lower()}):")
            print(f"  Start date time: '{energy_data.start_date_time}'")
            print(f"  Entries: {len(energy_data.entries)}")
            if energy_data.entries:
                print(f"  First entry: {energy_data.entries[0].to_dict()}")
            else:
                print(f"  No entries available")
            return energy_data
        except Exception as e:
            print(f"Error retrieving energy data: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_power_data(self, interval: PowerDataInterval, start_date_time: datetime, end_date_time: datetime):
        """
        Get power data from the P110 device with specified interval
        
        Args:
            interval: PowerDataInterval enum (Every5Minutes or Hourly)
            start_date_time: Start date and time for the data query (exclusive)
            end_date_time: End date and time for the data query (exclusive)
                          - For Every5Minutes: max 144 entries (12 hours), end_date_time will be adjusted if needed
                          - For Hourly: max 144 entries (6 days), end_date_time will be adjusted if needed
        
        Returns:
            Power data object if successful, None otherwise
        """
        device = await self._ensure_device_connected()
        if not device:
            print("Device not found or could not connect")
            return None
        
        try:
            power_data = await device.get_power_data(interval, start_date_time, end_date_time)
            interval_name = interval.name if hasattr(interval, 'name') else str(interval)
            print(f"\nPower data ({interval_name.lower()}):")
            print(f"  Start date time: '{power_data.start_date_time}'")
            print(f"  End date time: '{power_data.end_date_time}'")
            print(f"  Entries: {len(power_data.entries)}")
            if power_data.entries:
                print(f"  First entry: {power_data.entries[0].to_dict()}")
            else:
                print(f"  No entries available")
            return power_data
        except Exception as e:
            print(f"Error retrieving power data: {e}")
            import traceback
            traceback.print_exc()
            return None


