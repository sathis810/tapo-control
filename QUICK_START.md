# Quick Start Guide - Running on Another Computer

## Prerequisites
- Python 3.7 or higher installed
- Internet connection (for installing dependencies)

## Step-by-Step Instructions

### Option A: Using Setup Script (Easiest)

1. **Copy all project files** to the target computer:
   - `main.py`
   - `tapo_control.py`
   - `laptop_battery_loop.py`
   - `requirements.txt`
   - `env.example`
   - `setup.bat` (Windows) or `setup.sh` (Linux/Mac)
   - `README.md` (optional)

2. **Run the setup script**:
   - **Windows**: Double-click `setup.bat` or run `setup.bat` in Command Prompt
   - **Linux/Mac**: Run `bash setup.sh` or `chmod +x setup.sh && ./setup.sh`

3. **Configure environment**:
   - Copy `env.example` to `.env`
   - Open `.env` in a text editor
   - Fill in your credentials:
     ```
     TP_LINK_EMAIL=your-email@example.com
     TP_LINK_PASSWORD=your-password
     TAPO_DEVICE_IP=192.168.0.124
     BATTERY_START_THRESHOLD=40
     BATTERY_STOP_THRESHOLD=80
     BATTERY_CHECK_INTERVAL=60
     ```

4. **Run the application**:
   ```bash
   python main.py
   ```

### Option B: Manual Setup

1. **Copy project files** (same as Option A, step 1)

2. **Install dependencies manually**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (same as Option A, step 3)

4. **Run the application** (same as Option A, step 4)

### Option C: Install as Package

1. **On source computer**, build the package:
   ```bash
   pip install build wheel
   python -m build
   ```

2. **Copy `dist/` folder** to target computer

3. **Install the package**:
   ```bash
   pip install dist/tapo_control-1.0.0-py3-none-any.whl
   ```

4. **Configure environment** (create `.env` file as in Option A, step 3)

5. **Run the application**:
   ```bash
   python -m main
   ```

## Troubleshooting

### "Python is not recognized"
- Install Python from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

### "pip is not recognized"
- Try `python -m pip` instead of `pip`
- Or reinstall Python with "Add Python to PATH" checked

### Import errors
- Make sure dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.7+)

### Environment variables not working
- Ensure `.env` file exists in the same folder as `main.py`
- Check that `python-dotenv` is installed

### Device not found
- Verify `TAPO_DEVICE_IP` matches your device's IP address
- Ensure device is on the same network
- Check device is online in Tapo app

## What to Copy

**Required files:**
- `main.py`
- `tapo_control.py`
- `laptop_battery_loop.py`
- `requirements.txt`
- `env.example`

**Optional but helpful:**
- `setup.bat` / `setup.sh`
- `README.md`
- `PACKAGING.md`

**Do NOT copy:**
- `.env` (contains sensitive credentials - create new one)
- `__pycache__/` folder
- `dist/` folder (unless using package method)
- `.git/` folder

