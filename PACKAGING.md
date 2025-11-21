# Packaging and Distribution Guide

This guide explains how to package this project and run it on another computer.

## Method 1: Source Distribution (Recommended for Development)

### On Your Computer (Packaging)

1. **Install build tools** (if not already installed):
```bash
pip install build wheel
```

2. **Create source distribution**:
```bash
python -m build
```

This creates:
- `dist/tapo-control-1.0.0.tar.gz` (source distribution)
- `dist/tapo_control-1.0.0-py3-none-any.whl` (wheel distribution)

### On Another Computer (Installation)

1. **Copy the distribution files**:
   - Copy the entire `dist/` folder to the target computer
   - Or copy just the `.whl` file (wheel) for easier installation

2. **Install Python** (if not already installed):
   - Download from https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

3. **Install the package**:
```bash
# Using wheel (recommended)
pip install dist/tapo_control-1.0.0-py3-none-any.whl

# Or using source distribution
pip install dist/tapo-control-1.0.0.tar.gz

# Or directly from the folder
pip install .
```

4. **Set up environment**:
   - Copy `env.example` to `.env`
   - Edit `.env` with your credentials:
     ```
     TP_LINK_EMAIL=your-email@example.com
     TP_LINK_PASSWORD=your-password
     TAPO_DEVICE_IP=192.168.0.124
     BATTERY_START_THRESHOLD=40
     BATTERY_STOP_THRESHOLD=80
     BATTERY_CHECK_INTERVAL=60
     ```

5. **Run the application**:
```bash
python -m main
# Or if installed as package:
tapo-control
```

## Method 2: Simple File Copy (Easiest)

### Steps:

1. **On your computer**, create a package folder:
```bash
# Create a folder with all necessary files
mkdir tapo-package
```

2. **Copy all project files**:
   - `main.py`
   - `tapo_control.py`
   - `laptop_battery_loop.py`
   - `requirements.txt`
   - `env.example`
   - `README.md`

3. **Create a setup script** (`setup.bat` for Windows or `setup.sh` for Linux/Mac):

**Windows (`setup.bat`)**:
```batch
@echo off
echo Installing Tapo Control...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Copy env.example to .env
echo 2. Edit .env with your credentials
echo 3. Run: python main.py
pause
```

**Linux/Mac (`setup.sh`)**:
```bash
#!/bin/bash
echo "Installing Tapo Control..."
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy env.example to .env"
echo "2. Edit .env with your credentials"
echo "3. Run: python3 main.py"
```

4. **On another computer**:
   - Copy the entire `tapo-package` folder
   - Run `setup.bat` (Windows) or `setup.sh` (Linux/Mac)
   - Follow the instructions

## Method 3: Executable with PyInstaller (Standalone)

### On Your Computer:

1. **Install PyInstaller**:
```bash
pip install pyinstaller
```

2. **Create executable**:
```bash
pyinstaller --onefile --name tapo-control --add-data "env.example;." main.py
```

This creates `dist/tapo-control.exe` (Windows) or `dist/tapo-control` (Linux/Mac)

3. **Copy to another computer**:
   - Copy the executable file
   - Copy `env.example` and rename to `.env`
   - Edit `.env` with credentials
   - Run the executable

**Note**: The executable will be large (~50-100MB) but includes Python and all dependencies.

## Method 4: Docker Container (Advanced)

### Create Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### Build and run:

```bash
# Build image
docker build -t tapo-control .

# Run container
docker run -it --env-file .env tapo-control
```

## Quick Start Checklist for New Computer

- [ ] Python 3.7+ installed
- [ ] Project files copied
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created from `env.example`
- [ ] Credentials configured in `.env`
- [ ] Test run: `python main.py`

## Troubleshooting

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.7+)

### Environment Variables Not Loading
- Ensure `.env` file exists in the same directory as `main.py`
- Check that `python-dotenv` is installed

### Network Issues
- Verify `TAPO_DEVICE_IP` is correct for the new network
- Ensure device is on the same network (for local API)

### Battery Monitoring Not Working
- This feature only works on laptops with battery monitoring
- Desktop computers will show an error (this is expected)

## Distribution Files Checklist

When distributing, include:
- [ ] All Python source files (`.py`)
- [ ] `requirements.txt`
- [ ] `env.example`
- [ ] `README.md`
- [ ] `setup.py` and/or `pyproject.toml` (for Method 1)
- [ ] Setup script (`setup.bat` or `setup.sh` for Method 2)

