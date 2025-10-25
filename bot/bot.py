import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from misc.config import Config
from misc.rates_api import RatesApi
import time
import threading


def run_bot(initial_settings):
    token = initial_settings["token"]
    bot = telebot.TeleBot(token, parse_mode="HTML")
    config = Config("settings", "CryptoWatcher")
    settings = config.load() or initial_settings
    api = RatesApi()

    def save():
        config.save(settings)

    def allowed(uid):
        return uid in settings["whitelist"]

    def menu_main():
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("📈 Top coins", callback_data="top"))
        m.add(InlineKeyboardButton("⚙ Settings", callback_data="settings"))
        m.add(InlineKeyboardButton("🔔 Alerts", callback_data="alerts"))
        return m

    def menu_top():
        m = InlineKeyboardMarkup(row_width=2)
        for t in [("1h","1h"),("3h","3h"),("12h","12h"),("1d","1d"),("3d","3d"),("1w","1w"),("1m","1m"),("1y","1y"),("All","all")]:
            m.add(InlineKeyboardButton(t[0], callback_data=f"top_{t[1]}"))
        m.add(InlineKeyboardButton("⬅ Back", callback_data="back"))
        return m

    def menu_settings():
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("⏱ Interval", callback_data="interval"))
        m.add(InlineKeyboardButton("👤 Whitelist", callback_data="whitelist"))
        m.add(InlineKeyboardButton("⬅ Back", callback_data="back"))
        return m

    def menu_alerts():
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("➕ Add alert", callback_data="add_alert"))
        m.add(InlineKeyboardButton("🗑 Remove alert", callback_data="remove_alert"))
        m.add(InlineKeyboardButton("⬅ Back", callback_data="back"))
        return m

    @bot.message_handler(commands=["start"])
    def start(m):
        if not allowed(m.from_user.id):
            bot.send_message(m.chat.id, "⛔ Access denied.")
            return
        bot.send_message(m.chat.id, "Welcome!", reply_markup=menu_main())

    @bot.callback_query_handler(func=lambda c: True)
    def cb(call):
        uid = call.from_user.id
        if not allowed(uid):
            bot.answer_callback_query(call.id, "Access denied")
            return
        if call.data == "top":
            bot.edit_message_text("Top coins:", call.message.chat.id, call.message.id, reply_markup=menu_top())
        elif call.data.startswith("top_"):
            p = call.data.split("_")[1]
            try:
                t = api.get_search_trending()
                coins = t.get("coins", [])
                text = f"🔥 Trending coins ({p})\n\n"
                for c in coins[:10]:
                    item = c["item"]
                    text += f"{item['name']} ({item['symbol']}) Rank: {item['score']+1}\n"
                bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=menu_top())
            except Exception as e:
                bot.answer_callback_query(call.id, str(e))
        elif call.data == "settings":
            bot.edit_message_text("Settings:", call.message.chat.id, call.message.id, reply_markup=menu_settings())
        elif call.data == "alerts":
            bot.edit_message_text("Alerts:", call.message.chat.id, call.message.id, reply_markup=menu_alerts())
        elif call.data == "interval":
            bot.send_message(uid, f"Current interval: {settings['check_interval']} sec\nEnter new value:")
            bot.register_next_step_handler(call.message, set_interval)
        elif call.data == "whitelist":
            wl = ", ".join(map(str, settings["whitelist"])) or "empty"
            bot.send_message(uid, f"Current whitelist: {wl}\nEnter ID to add or remove:")
            bot.register_next_step_handler(call.message, manage_wl)
        elif call.data == "add_alert":
            bot.send_message(uid, "Enter alert in format: coin_id price(USD) (example: bitcoin 70000)")
            bot.register_next_step_handler(call.message, add_alert)
        elif call.data == "remove_alert":
            if not settings["alerts"]:
                bot.send_message(uid, "No alerts set.")
                return
            text = "Current alerts:\n"
            for i, a in enumerate(settings["alerts"]):
                text += f"{i+1}. {a['coin']} at {a['price']}$\n"
            bot.send_message(uid, text + "\nEnter number to remove:")
            bot.register_next_step_handler(call.message, remove_alert)
        elif call.data == "back":
            bot.edit_message_text("Main menu:", call.message.chat.id, call.message.id, reply_markup=menu_main())

    def set_interval(m):
        try:
            val = int(m.text.strip())
            settings["check_interval"] = val
            save()
            bot.send_message(m.chat.id, f"Interval changed to {val} sec.")
        except:
            bot.send_message(m.chat.id, "Invalid value.")

    def manage_wl(m):
        try:
            uid = int(m.text.strip())
            if uid in settings["whitelist"]:
                settings["whitelist"].remove(uid)
                msg = "removed"
            else:
                settings["whitelist"].append(uid)
                msg = "added"
            save()
            bot.send_message(m.chat.id, f"User {uid} {msg}.")
        except:
            bot.send_message(m.chat.id, "Invalid ID.")

    def add_alert(m):
        try:
            parts = m.text.strip().split()
            coin = parts[0]
            price = float(parts[1])
            settings["alerts"].append({"coin": coin, "price": price})
            save()
            bot.send_message(m.chat.id, f"Alert set for {coin} at {price}$")
        except:
            bot.send_message(m.chat.id, "Invalid format.")

    def remove_alert(m):
        try:
            idx = int(m.text.strip()) - 1
            if 0 <= idx < len(settings["alerts"]):
                rem = settings["alerts"].pop(idx)
                save()
                bot.send_message(m.chat.id, f"Removed alert for {rem['coin']} at {rem['price']}$")
            else:
                bot.send_message(m.chat.id, "Invalid number.")
        except:
            bot.send_message(m.chat.id, "Invalid number.")

    def auto_notify():
        while True:
            try:
                trending = api.get_search_trending()
                top = [c["item"]["name"] for c in trending.get("coins", [])[:3]]
                txt = "📊 Daily report:\n" + "\n".join(f"• {c}" for c in top)
                for uid in settings["whitelist"]:
                    bot.send_message(uid, txt)
                for a in settings["alerts"]:
                    price = api.get_price(a["coin"], "usd")[a["coin"]]["usd"]
                    if price >= a["price"]:
                        for uid in settings["whitelist"]:
                            bot.send_message(uid, f"🚨 {a['coin']} reached {price}$ (target {a['price']}$)")
                        settings["alerts"].remove(a)
                        save()
            except Exception as e:
                print("Notify error:", e)
            time.sleep(settings["check_interval"])

    threading.Thread(target=auto_notify, daemon=True).start()
    bot.infinity_polling()
