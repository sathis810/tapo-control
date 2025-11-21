"""
Helper script to create .env file from template
Run this script to set up your environment configuration
"""

import os
import shutil
from pathlib import Path

def create_env_file():
    """
    Create .env file from env.example template
    """
    current_dir = Path.cwd()
    env_example = current_dir / "env.example"
    env_file = current_dir / ".env"
    
    # Check if env.example exists
    if not env_example.exists():
        print("ERROR: env.example file not found!")
        print(f"Looking in: {current_dir}")
        print("\nPlease ensure env.example is in the current directory.")
        print("Or create .env manually with the following content:")
        print("\n" + "="*60)
        print("TP_LINK_EMAIL=your-email@example.com")
        print("TP_LINK_PASSWORD=your-password")
        print("TAPO_DEVICE_IP=192.168.0.124")
        print("BATTERY_START_THRESHOLD=40")
        print("BATTERY_STOP_THRESHOLD=80")
        print("BATTERY_CHECK_INTERVAL=60")
        print("="*60)
        return False
    
    # Check if .env already exists
    if env_file.exists():
        response = input(".env file already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Cancelled. .env file not modified.")
            return False
    
    # Copy env.example to .env
    try:
        shutil.copy(env_example, env_file)
        print("✓ Created .env file from env.example")
        print(f"  Location: {env_file}")
        print("\n⚠️  IMPORTANT: Please edit .env file and fill in your credentials:")
        print("   - TP_LINK_EMAIL")
        print("   - TP_LINK_PASSWORD")
        print("   - TAPO_DEVICE_IP")
        print("\nYou can edit it with:")
        print("   Windows: notepad .env")
        print("   Linux/Mac: nano .env")
        return True
    except Exception as e:
        print(f"ERROR: Failed to create .env file: {e}")
        return False


if __name__ == "__main__":
    print("="*60)
    print("Tapo Control - Environment Setup Helper")
    print("="*60)
    print()
    create_env_file()

