@echo off
echo ========================================
echo Tapo Control Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

echo Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Installing required dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy env.example to .env
echo 2. Edit .env with your credentials:
echo    - TP_LINK_EMAIL=your-email@example.com
echo    - TP_LINK_PASSWORD=your-password
echo    - TAPO_DEVICE_IP=your-device-ip
echo 3. Run: python main.py
echo.
pause

