sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt-get install python3.6 python3-venv -y
python3.6 -m pip install
pip3 install virtualenv
python3 -m venv ./venv
pyenv-3.6 ./venv
source ./venv/bin/activate
pip install -r requirements_python.txt
