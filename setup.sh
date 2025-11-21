#!/bin/bash

echo "========================================"
echo "Tapo Control Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org/downloads/"
    exit 1
fi

echo "Python found!"
python3 --version
echo ""

echo "Upgrading pip..."
python3 -m pip install --upgrade pip
echo ""

echo "Installing required dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Copy env.example to .env"
echo "2. Edit .env with your credentials:"
echo "   - TP_LINK_EMAIL=your-email@example.com"
echo "   - TP_LINK_PASSWORD=your-password"
echo "   - TAPO_DEVICE_IP=your-device-ip"
echo "3. Run: python3 main.py"
echo ""

