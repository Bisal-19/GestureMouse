#!/bin/bash

echo "=========================================="
echo "   Installing AI Gesture Mouse for Linux  "
echo "=========================================="

# 1. Update System & Install Linux Dependencies
# 'scrot' is needed for PyAutoGUI screenshots on Linux
# 'python3-tk' is needed for the GUI
echo "[*] Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv python3-tk scrot x11-utils

# 2. Create a Virtual Environment (Safe Mode)
echo "[*] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 3. Install Python Libraries
echo "[*] Installing Python libraries..."
pip install -r requirements.txt

# 4. Create a Run Script
echo "[*] Creating launcher script..."
echo '#!/bin/bash' > run.sh
echo 'source venv/bin/activate' >> run.sh
echo 'python3 Launcher.py' >> run.sh
chmod +x run.sh

echo "=========================================="
echo "      Installation Complete!              "
echo "      To start the app, run: ./run.sh     "
echo "=========================================="