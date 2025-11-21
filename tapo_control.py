"""
Tapo P110 Device Control Script
Controls Tapo P110 smart plugs via TP-Link Cloud API
"""

import os
import asyncio
from dotenv import load_dotenv
from tplinkcloud import TPLinkDeviceManager

# Load environment variables
load_dotenv()


class TapoP110Controller:
    """
    Controller class for Tapo P110 smart plug devices using cloud API
    """
    
    def __init__(self, email: str = None, password: str = None):
        """
        Initialize the Tapo P110 controller with cloud credentials
        
        Args:
            email: TP-Link cloud account email (or from .env file)
            password: TP-Link cloud account password (or from .env file)
        """
        self.email = email or os.getenv('TP_LINK_EMAIL')
        self.password = password or os.getenv('TP_LINK_PASSWORD')
        
        if not self.email or not self.password:
            raise ValueError("Email and password must be provided either as arguments or in .env file")
        
        self.device_manager = TPLinkDeviceManager(username=self.email, password=self.password)
        self.devices = None
    
    async def get_devices(self):
        """
        Retrieve list of all devices from TP-Link cloud
        
        Returns:
            List of device objects
        """
        try:
            # Login first (if not already logged in)
            login_result = self.device_manager.login(self.email, self.password)
            if login_result and hasattr(login_result, '__await__'):
                await login_result
            
            # Get devices
            devices_result = self.device_manager.get_devices()
            if devices_result and hasattr(devices_result, '__await__'):
                self.devices = await devices_result
            else:
                self.devices = devices_result
            
            return self.devices
        except Exception as e:
            print(f"Error retrieving devices: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    async def find_p110_device(self, device_alias: str = None):
        """
        Find a specific P110 device by alias or return first P110 device
        
        Args:
            device_alias: Optional device alias/name to search for
            
        Returns:
            Device object if found, None otherwise
        """
        if not self.devices:
            await self.get_devices()
        
        if not self.devices:
            print("No devices found")
            return None
        
        if device_alias:
            for device in self.devices:
                if device.get_alias().lower() == device_alias.lower():
                    return device
            print(f"Device '{device_alias}' not found")
            return None
        
        # Return first device if no alias specified
        return self.devices[0] if self.devices else None
    
    async def turn_on(self, device_alias: str = None):
        """
        Turn on a P110 device
        
        Args:
            device_alias: Optional device alias/name. If not provided, uses first device
            
        Returns:
            True if successful, False otherwise
        """
        device = await self.find_p110_device(device_alias)
        if not device:
            print("Device not found")
            return False
        
        try:
            # Check current status before turning on
            is_currently_off = await device.is_off()
            is_currently_on = await device.is_on()
            
            # Handle None returns (device info unavailable)
            if is_currently_off is None or is_currently_on is None:
                print(f"Warning: Could not determine current status for device '{device.get_alias()}'")
                print("  Proceeding with turn on command anyway...")
            else:
                status_str = "ON" if is_currently_on else "OFF"
                print(f"Device '{device.get_alias()}' current status: {status_str}")
            
            # Turn on the device - directly await the async method
            print(f"Executing power_on command for device '{device.get_alias()}'...")
            try:
                result = await device.power_on()
                if result is None:
                    print(f"[OK] Command executed successfully (response: None - this is normal for cloud API)")
                else:
                    print(f"[OK] Command executed. Response: {result}")
            except Exception as cmd_error:
                print(f"[ERROR] Error executing power_on command: {cmd_error}")
                import traceback
                traceback.print_exc()
                return False
            
            # Wait a moment for the command to process and device state to update
            await asyncio.sleep(3)  # Increased wait time for cloud API
            
            # Refresh device state by getting fresh status
            await self.get_devices()  # Refresh device list
            device = await self.find_p110_device(device_alias)
            
            if device:
                # Verify the device is actually on
                is_now_on = await device.is_on()
                is_now_off = await device.is_off()
                
                if is_now_on is True and is_now_off is False:
                    print(f"[SUCCESS] Successfully turned ON: {device.get_alias()}")
                    return True
                elif is_now_on is None or is_now_off is None:
                    print(f"[INFO] Command executed, but could not verify device status")
                    print(f"  This may be normal for cloud API - status checks sometimes return None")
                    print(f"  Please check the physical device to confirm it turned on")
                    print(f"  If the device did turn on, the command was successful!")
                    return True  # Assume success if command executed without error
                else:
                    current_status = "ON" if is_now_on else "OFF"
                    print(f"[WARNING] Device '{device.get_alias()}' status is still {current_status}")
                    print(f"  The turn on command may not have worked. Please check the device manually.")
                    return False
            else:
                print("[ERROR] Could not verify device status - device not found after refresh")
                return False
        except Exception as e:
            print(f"[ERROR] Error turning device on: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def turn_off(self, device_alias: str = None):
        """
        Turn off a P110 device
        
        Args:
            device_alias: Optional device alias/name. If not provided, uses first device
            
        Returns:
            True if successful, False otherwise
        """
        device = await self.find_p110_device(device_alias)
        if not device:
            print("Device not found")
            return False
        
        try:
            # Check current status before turning off
            is_currently_on = await device.is_on()
            is_currently_off = await device.is_off()
            
            # Handle None returns (device info unavailable)
            if is_currently_off is None or is_currently_on is None:
                print(f"Warning: Could not determine current status for device '{device.get_alias()}'")
                print("  Proceeding with turn off command anyway...")
            else:
                status_str = "ON" if is_currently_on else "OFF"
                print(f"Device '{device.get_alias()}' current status: {status_str}")
            
            # Turn off the device - directly await the async method
            print(f"Executing power_off command for device '{device.get_alias()}'...")
            try:
                result = await device.power_off()
                if result is None:
                    print(f"[OK] Command executed successfully (response: None - this is normal for cloud API)")
                else:
                    print(f"[OK] Command executed. Response: {result}")
            except Exception as cmd_error:
                print(f"[ERROR] Error executing power_off command: {cmd_error}")
                import traceback
                traceback.print_exc()
                return False
            
            # Wait a moment for the command to process and device state to update
            await asyncio.sleep(3)  # Increased wait time for cloud API
            
            # Refresh device state by getting fresh status
            await self.get_devices()  # Refresh device list
            device = await self.find_p110_device(device_alias)
            
            if device:
                # Verify the device is actually off
                is_now_off = await device.is_off()
                is_now_on = await device.is_on()
                
                if is_now_off is True and is_now_on is False:
                    print(f"[SUCCESS] Successfully turned OFF: {device.get_alias()}")
                    return True
                elif is_now_off is None or is_now_on is None:
                    print(f"[INFO] Command executed, but could not verify device status")
                    print(f"  This may be normal for cloud API - status checks sometimes return None")
                    print(f"  Please check the physical device to confirm it turned off")
                    print(f"  If the device did turn off, the command was successful!")
                    return True  # Assume success if command executed without error
                else:
                    current_status = "ON" if is_now_on else "OFF"
                    print(f"[WARNING] Device '{device.get_alias()}' status is still {current_status}")
                    print(f"  The turn off command may not have worked. Please check the device manually.")
                    return False
            else:
                print("[ERROR] Could not verify device status - device not found after refresh")
                return False
        except Exception as e:
            print(f"[ERROR] Error turning device off: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def get_device_info(self, device_alias: str = None):
        """
        Get information about a P110 device
        
        Args:
            device_alias: Optional device alias/name. If not provided, uses first device
            
        Returns:
            Device object
        """
        device = await self.find_p110_device(device_alias)
        if device:
            print(f"\nDevice Information:")
            print(f"  Alias: {device.get_alias()}")
            try:
                sys_info = await device.get_sys_info()
                if sys_info:
                    print(f"  Model: {sys_info.get('model', 'N/A')}")
                    print(f"  Device ID: {sys_info.get('deviceId', 'N/A')}")
                    print(f"  Hardware Version: {sys_info.get('hw_ver', 'N/A')}")
                    print(f"  Firmware Version: {sys_info.get('fw_ver', 'N/A')}")
            except Exception as e:
                print(f"  (Could not retrieve system info: {e})")
            return device
        return None
    
    async def get_device_status(self, device_alias: str = None):
        """
        Get the current power status of a device
        
        Args:
            device_alias: Optional device alias/name. If not provided, uses first device
            
        Returns:
            String status: "ON" or "OFF"
        """
        device = await self.find_p110_device(device_alias)
        if not device:
            return None
        
        try:
            is_on_status = await device.is_on()
            return "ON" if is_on_status else "OFF"
        except Exception as e:
            print(f"Error getting device status: {e}")
            return None
    
    async def list_all_devices(self):
        """
        List all available devices with their information
        """
        if not self.devices:
            await self.get_devices()
        
        if not self.devices:
            print("No devices found")
            return
        
        print(f"\nFound {len(self.devices)} device(s):")
        for i, device in enumerate(self.devices, 1):
            print(f"\n{i}. {device.get_alias()}")
            try:
                sys_info = await device.get_sys_info()
                if sys_info:
                    print(f"   Model: {sys_info.get('model', 'N/A')}")
                    print(f"   Device ID: {sys_info.get('deviceId', 'N/A')}")
                # Show current status
                status = await self.get_device_status(device.get_alias())
                if status:
                    print(f"   Status: {status}")
            except Exception as e:
                print(f"   Error getting info: {e}")


async def main():
    """
    Example usage of TapoP110Controller
    """
    try:
        # Initialize controller
        controller = TapoP110Controller()
        
        # List all devices
        await controller.list_all_devices()
        
        # Get device alias from environment variable (optional)
        device_alias = os.getenv('TAPO_DEVICE_ALIAS')
        
        # Check current status
        status = await controller.get_device_status(device_alias)
        print(f"\nCurrent device status: {status}")
        
        # Example: Turn on device (uses env variable if set, otherwise None uses first device)
        await controller.turn_on(device_alias)
        
        # Example: Turn off specific device by alias
        result = await controller.turn_off(device_alias)
        if result:
            print("Turn off command executed successfully")
        else:
            print("Turn off command failed")
        
        # Verify final status
        final_status = await controller.get_device_status(device_alias)
        print(f"Final device status: {final_status}")
        
        # Example: Get device info
        await controller.get_device_info(device_alias)
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set TP_LINK_EMAIL and TP_LINK_PASSWORD in .env file")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

