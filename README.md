# Crepitus

[![Github Issues](https://img.shields.io/github/issues/Stonks-Luma-Liberty/Crepitus?logo=github\&style=for-the-badge)](https://github.com/Stonks-Luma-Liberty/Crepitus/issues)
[![Codacy Badge](https://img.shields.io/codacy/grade/959e4a142b3043d4b4dbf94646c680a8?logo=codacy\&style=for-the-badge)](https://www.codacy.com/gh/Stonks-Luma-Liberty/Crepitus/dashboard?utm_source=github.com\&utm_medium=referral\&utm_content=Stonks-Luma-Liberty/Crepitus\&utm_campaign=Badge_Grade)
[![Github Top Language](https://img.shields.io/github/languages/top/Stonks-Luma-Liberty/Crepitus?logo=python\&style=for-the-badge)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

Gas tracking bot for various crypto currencies. (Currently only supports ethereum)

## Table of Contents

*   [Features](#features)

*   [Environment Variables](#environment-variables)

*   [Run Locally](#run-locally)

    *   [With Docker](#with-docker)
    *   [Without Docker](#without-docker)

## Features

*   Displays gas fees on ethereum
*   Provides rough estimation of gas spent in USD

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DISCORD_BOT_TOKEN` - Token required to connect with your discord bot

`ETHERSCAN_API_KEY` - Api Key to access Etherscan

`ETHEREUM_MAIN_NET_URL` - Web3 HTTP provider to use for ethereum

## Run Locally

Clone the project

```bash
  git clone https://github.com/Stonks-Luma-Liberty/Crepitus.git
```

Go to the project directory

```bash
  cd Crepitus
```

### With Docker

Use docker-compose to start the bot

```bash
docker-compose up -d --build
```

### Without Docker

Install dependencies

```bash
  poetry install
```

Start the bot

```bash
  poetry run python main.py
```
