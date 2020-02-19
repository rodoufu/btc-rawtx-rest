#!/usr/bin/env bash
sudo apt-get install -y python3-venv
mkdir -p venv
cd venv
python3 -m venv env

source venv/env/bin/activate
pip3 install -r requirements.txt
pip3 install connexion[swagger-ui]
