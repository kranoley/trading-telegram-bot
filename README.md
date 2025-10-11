# Telegram Bot for Trading

A Telegram bot for tracking cryptocurrency prices and setting price alerts.  
Uses **pyTelegramBotAPI** and **CoinGecko API** for market data.

---



## Features


- Verifies the ability to send messages to the admin.
- Stores all settings in a secure configuration file.
- Inline main menu with sections:
  - **Top coins** — displays trending cryptocurrencies.
  - **Settings** — manage whitelist and check interval.
  - **Alerts** — add or remove price alerts.
- Automatic notifications about trending coins and price triggers.
- Whitelist control and customizable check interval directly in Telegram.

---

## Requirements

- Python 3.5+
- Dependencies:
  ```bash
  pip install pyTelegramBotAPI pycoingecko
  ```

---

## Installation

1. [Download the source code](https://github.com/kranoley/trading-telegram-bot/archive/refs/heads/main.zip)
2. Extract the archive to any folder.
3. Run:
   ```bash
   python main.py
   ```
4. On first launch you will be asked to enter:
   - **Bot token**
   - **Admin ID**

If successful, the admin will receive the message:
```
✅ Bot successfully started.
```

---

## How to Create a Telegram Bot
![tgbot](https://i.imgur.com/sQ098Ed.jpeg)
1. Open Telegram and find [@BotFather](https://t.me/BotFather).
2. Send:
   ```
   /newbot
   ```
3. Follow the instructions and get your token, for example:
   ```
   1234567890:ABCdefGhIJKlmNoPQRstuVWxyz123456789
   ```
4. Use this token when launching `main.py` for the first time.

---

## How to Get Your Telegram ID

1. Open [@userinfobot](https://t.me/userinfobot) in Telegram.
2. Send:
   ```
   /start
   ```
3. You will receive a message like:
   ```
   Id: 123456789
   ```
   Use this number as your `admin_id` when starting the bot.

![tgid](https://i.imgur.com/B4nYSQH.jpeg)
---



