#!/bin/bash

wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.110/linux64/chromedriver-linux64.zip -p /tmp/chromedriver
cd /tmp/chromedriver/
unzip chromedriver-linux64.zip
mv /tmp/chromedriver/chromedriver-linux64/chromedriver /opt/supersub_monitor/drivers/chromedriver_linux
