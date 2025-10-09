import telebot
from misc.config import Config
import os
from bot.bot import run_bot

config = Config("settings", "CryptoWatcher")
settings = config.load()

if not settings:
    settings = {"token": "", "admin_id": 0, "whitelist": [], "check_interval": 3600, "alerts": []}

if not settings["token"]:
    settings["token"] = input("Enter bot token: ").strip()
if not settings["admin_id"]:
    settings["admin_id"] = int(input("Enter admin ID: ").strip())

bot = telebot.TeleBot(settings["token"], parse_mode="HTML")

try:
    bot.send_message(settings["admin_id"], "✅ Bot successfully started.")
except Exception as e:
    print("❌ Unable to send message to admin:", e)
    exit(1)

if settings["admin_id"] not in settings["whitelist"]:
    settings["whitelist"].append(settings["admin_id"])

config.save(settings)
run_bot(settings)
