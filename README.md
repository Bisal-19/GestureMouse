# 🖱️ AI Gesture Mouse

A touch-free mouse controller built with Python, OpenCV, and MediaPipe. Control your mouse just by moving your hands!

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

## 🔧 Linux Troubleshooting

If you see an error like `Xlib.error.DisplayConnectionError`, it means your specific Linux setup (Wayland) is blocking the app.

**Solution 1 (Quick Fix):**
Run this command in your terminal before starting the app:
```bash
    xhost +SI:localuser:$(whoami)

**Solution 2 (Recommended):

-Log out of Ubuntu.

-Click the Gear Icon ⚙️ on the login screen.

-Select Ubuntu on Xorg.

-Log back in and run the app.

🛠️ Requirements
   . Webcam

   . Good lighting for best accuracy

   . Python 3.9+ (If running from source manually)