#!/bin/bash

cd /opt/supersub_monitor
sudo git pull
sudo systemctl restart supersub
