#!/bin/bash

cd /opt/supersub_monitor
logger "Pulling new version"
sudo git pull

logger "Installing requirements"
sudo .venv/bin/pip install -r requirements.txt

HEAD=$(git rev-parse --short HEAD)
logger "Launching commit: $HEAD"
sudo systemctl restart supersub

logger "Service restarted"
