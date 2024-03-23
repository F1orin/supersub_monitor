#!/bin/bash

# Function to log messages with timestamp
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

# Log start message
log "Updating Chromedriver and Google Chrome Stable..."

# Retrieve JSON data from the URL
log "Fetching latest Chromedriver URL..."
json_data=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json)

# Parse JSON and extract the Chromedriver URL for Linux 64-bit
chromedriver_url=$(echo "$json_data" | jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform == "linux64") | .url')

# Download the latest Chromedriver
log "Downloading latest Chromedriver..."
wget "$chromedriver_url" -P /tmp/chromedriver
cd /tmp/chromedriver || { log "Failed to change directory to /tmp/chromedriver"; exit 1; }
unzip -o chromedriver-linux64.zip

# Move the new Chromedriver to the specified location
log "Moving Chromedriver to /opt/supersub_monitor/drivers/..."
sudo mv /tmp/chromedriver/chromedriver-linux64/chromedriver /opt/supersub_monitor/drivers/chromedriver_linux

# Upgrade Google Chrome Stable
log "Upgrading Google Chrome Stable..."
sudo apt-get install --only-upgrade google-chrome-stable

# Log completion message
log "Chromedriver and Google Chrome Stable have been updated successfully."
