# Supersub Monitor

An application that reports available matches for an UrbanSoccer Supersub to a Telegram bot.

<img src="https://github.com/F1orin/supersub_monitor/blob/main/Screenshot.jpg" width="200" alt="Telegram bot message showing Supersub matches availability">

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Introduction

In France, there is a network of football fields called UrbanSoccer. This network has a web portal, where among other possibilities there is a feature of matching players without a team with teams in need of substitutes — it's called Supersub.

I felt the need to receive the reports about available matches easier and quicker compared to visiting the web portal, and that's how this application appeared.

## Features

* Built with Python
* Scrapes the UrbanSoccer web portal using Selenium and ChromeDriver
* Automatically gets latest ChromeDriver using webdriver-manager
* Integration with Telegram powered by python-telegram-bot
* Continuous Deployment implemented with GitHub Actions
* Deployed on Google Cloud Platform, on a free tier Compute Engine VM
* Wrapped in systemd service

## Deployment

1. Provision a Virtual Machine
2. Clone the repository onto the host:
    ```
    sudo git clone https://github.com/F1orin/supersub_monitor.git /opt/supersub_monitor
    cd /opt/supersub_monitor
    ```
3. Create python's virtual environment:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4. Install dependencies:
    ```
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
5. Populate the required environment variables:
    ```
    cp src/.env.template src/.env
    nano src/.env
    ```
    1. Set the city (e.g. `Nantes`)
    2. Provide UrbanSoccer credentials (Browser dev tools -> Application -> Local storage, look for `auth-token` and `auth-userid`)
    3. Configure Telegram bot - see [here](https://telegram.me/BotFather)
6. Install and start the supersub systemd service.
    ```
    sudo cp deploy/supersub.service /etc/systemd/system/supersub.service
    sudo systemctl daemon-reload
    sudo systemctl enable --now supersub
    ```

Tip: rebooting the GCE instance changes its public IP, so remember to update the SSH_HOST secret in GitHub Actions before the next deploy.

## Contributing

If you would like to contribute, please submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
