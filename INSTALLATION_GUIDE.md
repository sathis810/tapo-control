# Installation and Environment Setup Guide

## What Happens When You Install the Package

When you run `pip install dist/tapo_control-1.0.0-py3-none-any.whl`, the following happens:

### ✅ What Gets Installed:

1. **Python Modules** (installed to your Python site-packages):
   - `tapo_control.py` - Tapo device control module
   - `laptop_battery_loop.py` - Battery monitoring module
   - `main.py` - Main application entry point

2. **Dependencies** (automatically installed):
   - `tapo>=0.8.7` - Tapo API client
   - `python-dotenv>=1.0.0` - Environment variable loader
   - `psutil>=5.9.0` - System and battery information

3. **Command Line Tool**:
   - `tapo-control` command becomes available (if entry point works)

### ❌ What Does NOT Get Installed:

- `.env` file (contains your credentials - must be created manually)
- `env.example` file (template file - you need to copy this)
- `README.md` and other documentation files

## Step-by-Step Setup After Installation

### Step 1: Verify Installation

Check that the package is installed:
```bash
pip show tapo-control
```

You should see package information including version 1.0.0.

### Step 2: Create Your Working Directory

Create a folder where you'll run the application:
```bash
mkdir tapo-control-app
cd tapo-control-app
```

### Step 3: Create the `.env` File

The application needs a `.env` file in the **current working directory** where you run the application.

**Option A: Manual Creation**

1. Create a new file named `.env` (note the dot at the beginning)
2. Copy this template and fill in your values:

```env
# Tapo Account Credentials
TP_LINK_EMAIL=your-email@example.com
TP_LINK_PASSWORD=your-password

# Required: Device IP address on your local network
TAPO_DEVICE_IP=192.168.0.124

# Battery Charging Thresholds (optional - defaults shown)
BATTERY_START_THRESHOLD=40
BATTERY_STOP_THRESHOLD=80
BATTERY_CHECK_INTERVAL=60
```

**Option B: Copy from Source**

If you have access to the original project files:
```bash
# Copy env.example to your working directory
copy env.example .env
# (On Linux/Mac: cp env.example .env)

# Then edit .env with your credentials
notepad .env
# (On Linux/Mac: nano .env or vim .env)
```

### Step 4: Fill in Your Credentials

Edit the `.env` file and replace:

- `your-email@example.com` → Your TP-Link/Tapo account email
- `your-password` → Your TP-Link/Tapo account password
- `192.168.0.124` → Your Tapo P110 device's IP address on your local network

**How to find your device IP:**
- Check your router's admin panel (connected devices list)
- Use the Tapo app → Device Settings → Device Info
- Or use network scanning tools

### Step 5: Run the Application

Now you can run the application from your working directory:

**Method 1: Using Python module**
```bash
python -m main
```

**Method 2: Using entry point (if available)**
```bash
tapo-control
```

**Method 3: Interactive Python**
```python
python
>>> from main import main
>>> import asyncio
>>> asyncio.run(main())
```

## Important Notes

### Where Should the `.env` File Be?

The `.env` file must be in the **current working directory** where you run the application, NOT in the Python installation directory.

**Example:**
```
C:\Users\YourName\tapo-control-app\    ← Create .env here
├── .env                                ← Application looks here
└── (run python -m main from here)
```

### Environment Variable Loading

The application uses `python-dotenv` which:
- Looks for `.env` in the current working directory
- Loads variables when the application starts
- Does NOT require system environment variables

### Security Reminders

⚠️ **Never commit `.env` to version control**
⚠️ **Keep your `.env` file secure and private**
⚠️ **Don't share your `.env` file with others**

## Troubleshooting

### Error: "Email and password must be provided"

**Problem:** The `.env` file is missing or not in the correct location.

**Solution:**
1. Make sure `.env` exists in your current working directory
2. Check that you're running the app from the same directory where `.env` is located
3. Verify `.env` file has correct format (no spaces around `=`)

### Error: "Device not found" or Connection errors

**Problem:** Incorrect device IP address or network issues.

**Solution:**
1. Verify `TAPO_DEVICE_IP` matches your device's actual IP
2. Ensure device is on the same network
3. Check device is online in Tapo app

### Error: Module not found

**Problem:** Package not installed correctly.

**Solution:**
```bash
pip uninstall tapo-control
pip install dist/tapo_control-1.0.0-py3-none-any.whl
```

### Application can't find `.env` file

**Problem:** Running from wrong directory.

**Solution:**
```bash
# Check current directory
pwd  # Linux/Mac
cd   # Windows

# Navigate to directory with .env file
cd path/to/your/tapo-control-app

# Then run
python -m main
```

## Quick Setup Script

Create a `setup_env.bat` (Windows) or `setup_env.sh` (Linux/Mac) file:

**Windows (`setup_env.bat`):**
```batch
@echo off
echo Creating .env file...
copy env.example .env
echo.
echo Please edit .env file with your credentials:
echo   - TP_LINK_EMAIL
echo   - TP_LINK_PASSWORD  
echo   - TAPO_DEVICE_IP
echo.
notepad .env
```

**Linux/Mac (`setup_env.sh`):**
```bash
#!/bin/bash
echo "Creating .env file..."
cp env.example .env
echo ""
echo "Please edit .env file with your credentials:"
echo "  - TP_LINK_EMAIL"
echo "  - TP_LINK_PASSWORD"
echo "  - TAPO_DEVICE_IP"
echo ""
nano .env
```

## Summary Checklist

After installing the package, make sure you have:

- [ ] Package installed (`pip show tapo-control`)
- [ ] Created a working directory
- [ ] Created `.env` file in working directory
- [ ] Filled in `TP_LINK_EMAIL` in `.env`
- [ ] Filled in `TP_LINK_PASSWORD` in `.env`
- [ ] Filled in `TAPO_DEVICE_IP` in `.env`
- [ ] Verified device IP is correct
- [ ] Run application from directory containing `.env`

Once all checked, you're ready to use the application! 🎉

