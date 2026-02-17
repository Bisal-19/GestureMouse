# 🖱️ AI Gesture Mouse

A touch-free mouse controller built with Python, OpenCV, and MediaPipe. Control your computer entirely with hand gestures!

![Gesture Demo](https://img.shields.io/badge/Status-Active-success) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue)

## ✨ Features
- **👆 Move Cursor:** Point with your Index finger.
- **🖱️ Left Click:** Pinch your Index + Middle fingers.
- **📦 Drag & Drop:** Pinch and hold (Index + Middle) while moving.
- **🔘 Right Click:** Pinch your Thumb + Index fingers.
- **📜 Scroll:** Raise your Pinky finger and move hand up/down.

---

## 📥 Download & Install

### 🪟 Windows Users
1. Go to the **[Releases Page](../../releases)** on the right.
2. Download the latest `GestureMouse.exe`.
3. Run it! (No installation required).

### 🐧 Linux Users
Open your terminal and run these commands to install from source:

```bash
# 1. Download the code
git clone [https://github.com/Bisal-19/GestureMouse.git](https://github.com/Bisal-19/GestureMouse.git)

# 2. Enter the folder
cd GestureMouse

# 3. Make the installer executable
chmod +x install.sh

# 4. Install and Run
./install.sh

🔧 Troubleshooting (Common Errors)
If the app isn't working, check the solutions below for your specific error.

🔴 Error 1: "Xlib.error.DisplayConnectionError"
Cause: Your Linux system is using Wayland (default on Ubuntu), which blocks screen control apps for security.
Solution:
Run this command in your terminal before starting the app:

xhost +SI:localuser:$(whoami)
If that doesn't work: Log out of Ubuntu, click the Gear Icon ⚙️ on the login screen, and select "Ubuntu on Xorg".

🔴 Error 2: "AttributeError: module 'mediapipe' has no attribute 'solutions'"
Cause: You have an incompatible version of MediaPipe.
Solution:
Run these commands to install the correct version:

source venv/bin/activate
pip install mediapipe==0.10.14

🛠️ Requirements
- Webcam

- Good lighting for best accuracy

- Python 3.10+ (If running from source manually)

