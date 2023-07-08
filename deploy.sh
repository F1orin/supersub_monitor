#!/bin/bash

cd /opt/supersub_monitor
logger "Pulling new version"
sudo git pull
HEAD=$(git rev-parse --short HEAD)
logger "Launching commit: $HEAD"
sudo systemctl restart supersub
logger "Service restarted"
