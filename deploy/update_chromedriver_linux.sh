#!/bin/bash

CHROMEDRIVER_URL="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/linux64/chromedriver-linux64.zip"

wget "$CHROMEDRIVER_URL" -P /tmp/chromedriver
cd /tmp/chromedriver/ || exit
unzip chromedriver-linux64.zip
mv /tmp/chromedriver/chromedriver-linux64/chromedriver /opt/supersub_monitor/drivers/chromedriver_linux
