# Setup environment on Pi
sudo apt install libjpeg9-dev zlib1g-dev python3-pil
python3 -m venv pisolar
source pisolar/bin/activate
cd pisolar
pip install --upgrade pip
