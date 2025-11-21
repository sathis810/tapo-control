# Tapo P110 Cloud Control

Python project to control Tapo P110 smart plugs via TP-Link Cloud API.

## Features

- ✅ Cloud-based control (works from anywhere with internet)
- ✅ Turn devices ON/OFF remotely
- ✅ List all connected devices
- ✅ Get device information
- ✅ Support for multiple P110 devices

## Prerequisites

- Python 3.7 or higher
- TP-Link cloud account (same credentials used in Tapo app)
- Tapo P110 device(s) already set up and connected to TP-Link cloud

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your credentials:
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your TP-Link cloud account credentials:
   ```
   TP_LINK_EMAIL=your-email@example.com
   TP_LINK_PASSWORD=your-password
   ```

## Usage

### Basic Usage

```python
from tapo_control import TapoP110Controller

# Initialize controller (reads credentials from .env)
controller = TapoP110Controller()

# List all devices
controller.list_all_devices()

# Turn on first device
controller.turn_on()

# Turn off specific device by name
controller.turn_off("Living Room Plug")

# Get device information
controller.get_device_info("Bedroom Plug")
```

### Command Line Usage

Run the example script:
```bash
python tapo_control.py
```

### Advanced Usage

You can also pass credentials directly:

```python
controller = TapoP110Controller(
    email="your-email@example.com",
    password="your-password"
)
```

## API Methods

### `TapoP110Controller` Class

- **`get_devices()`** - Retrieve all devices from cloud
- **`find_p110_device(device_alias)`** - Find device by alias
- **`turn_on(device_alias)`** - Turn device ON
- **`turn_off(device_alias)`** - Turn device OFF
- **`get_device_info(device_alias)`** - Get device information
- **`list_all_devices()`** - List all available devices

## Example Script

```python
from tapo_control import TapoP110Controller

# Initialize
controller = TapoP110Controller()

# List devices
controller.list_all_devices()

# Control device
controller.turn_on("My P110 Plug")
# ... do something ...
controller.turn_off("My P110 Plug")
```

## Security Notes

- ⚠️ Never commit your `.env` file to version control
- ⚠️ Keep your TP-Link credentials secure
- ⚠️ This library uses unofficial API - use at your own risk

## Troubleshooting

### Authentication Errors
- Verify your email and password are correct
- Ensure your TP-Link account is active
- Check that your P110 device is connected to TP-Link cloud

### Device Not Found
- Make sure device is set up in Tapo app
- Verify device is online and connected to cloud
- Check device alias/name matches exactly (case-sensitive)

## Library Information

This project uses `tplink-cloud-api` library:
- GitHub: https://github.com/piekstra/tplink-cloud-api
- Note: This is an unofficial, community-developed library

## License

This project is provided as-is for educational and personal use.

