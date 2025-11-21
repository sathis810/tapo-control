# What Happens After `pip install` - Quick Reference

## ✅ What Gets Installed

When you run:
```bash
pip install dist/tapo_control-1.0.0-py3-none-any.whl
```

**Installed:**
- ✅ Python modules (`tapo_control`, `laptop_battery_loop`, `main`)
- ✅ All dependencies (`tapo`, `python-dotenv`, `psutil`)
- ✅ Command line tool `tapo-control` (if entry point works)

**NOT Installed:**
- ❌ `.env` file (you must create this manually)
- ❌ Configuration files

## 🔧 What You Need to Do Next

### 1. Create a Working Directory
```bash
mkdir my-tapo-app
cd my-tapo-app
```

### 2. Create `.env` File

**Option A: Manual creation**
Create a file named `.env` with:
```env
TP_LINK_EMAIL=your-email@example.com
TP_LINK_PASSWORD=your-password
TAPO_DEVICE_IP=192.168.0.124
BATTERY_START_THRESHOLD=40
BATTERY_STOP_THRESHOLD=80
BATTERY_CHECK_INTERVAL=60
```

**Option B: Use helper script** (if you have `env.example` and `create_env.py`)
```bash
python create_env.py
# Then edit .env with your credentials
```

### 3. Fill in Your Credentials

Edit `.env` and replace:
- `your-email@example.com` → Your Tapo account email
- `your-password` → Your Tapo account password  
- `192.168.0.124` → Your device's IP address

### 4. Run the Application

From the directory containing `.env`:
```bash
python -m main
```

## 📍 Important: Where to Put `.env`

The `.env` file must be in the **same directory** where you run the application:

```
my-tapo-app/          ← Your working directory
├── .env              ← Put .env here
└── (run python -m main from here)
```

**NOT** in:
- Python installation directory
- Site-packages folder
- Anywhere else

## 🚀 Quick Start Example

```bash
# 1. Install package
pip install dist/tapo_control-1.0.0-py3-none-any.whl

# 2. Create working directory
mkdir tapo-app && cd tapo-app

# 3. Create .env file
echo TP_LINK_EMAIL=your-email@example.com > .env
echo TP_LINK_PASSWORD=your-password >> .env
echo TAPO_DEVICE_IP=192.168.0.124 >> .env

# 4. Edit .env with your actual credentials
notepad .env  # Windows
# or
nano .env     # Linux/Mac

# 5. Run application
python -m main
```

## ❓ Common Questions

**Q: Where is the .env file located after installation?**  
A: It's NOT installed. You must create it manually in your working directory.

**Q: Can I put .env anywhere?**  
A: No, it must be in the current working directory where you run `python -m main`.

**Q: How do I know if installation worked?**  
A: Run `pip show tapo-control` - you should see package info.

**Q: The app says "Email and password must be provided"**  
A: Make sure `.env` exists in the directory where you're running the app.

## 📚 More Help

- Full installation guide: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- Packaging instructions: [PACKAGING.md](PACKAGING.md)

