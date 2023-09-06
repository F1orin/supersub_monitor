# Supersub Monitor

An application that reports to Telegram bot available matches for UrbanSoccer Supersub.

<img src="https://github.com/F1orin/supersub_monitor/blob/main/Screenshot.jpg" width="200">

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Introduction

In France there is a network of football fields called UrbanSoccer. This network has a web portal, where among other possibilities there is a feature of matching players without a team with the teams in need of substitutes, it's called Supersub.

I felt the need of receiving the reports about available matches easier and quicker compared to visiting the web portal, that's how this application appeared.


## Features

* Written in Python
* Tested with pytest
* Scrapes the UrbanSoccer web portal using Selenium and ChromeDriver
* Integration with Telegram powered by python-telegram-bot
* Continuous Deployment implemented with GitHub Actions
* Deployed on Google Cloud Platform, on a free tier Compute Engine VM
* Wrapped in systemd service


## Installation

1. Create VM
2. Clone the repo
3. Create venv
4. Install python requirements
5. Download ChromeDriver and put it to the right place
6. Configure environment variables
    1. Set the city
    2. Provide UrbanSoccer credentials
    3. Configure Telegram bot
7. Create and run systemd service


## Usage

Telegram bot supports these commands:
* /check - to receive the list of available matches
* /help - to see the help message with supported commands


## Contributing

If you would like to contribute, please submit a pull request.


## License

This project is licensed under the [MIT License](LICENSE).
