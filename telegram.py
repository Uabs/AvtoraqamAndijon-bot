import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_PHONE = "+998 99 434 10 00"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=["start"])
def start(message):
    print("START KELDI:", message.chat.id)

    text = f"""
🚘 Avtoraqam Andijon

Assalomu alaykum!

📞 Avtoraqam sotib olish yoki
ma'lumot olish uchun admin bilan bog'laning:

{ADMIN_PHONE}
"""

    bot.send_message(message.chat.id, text)


@app.route("/")
def home():
    return "Avtoraqam Andijon Bot ishlayapti!", 200


@app.route("/webhook", methods=["POST"])
def webhook():

    try:
        data = request.get_data().decode("utf-8")

        print("WEBHOOK KELDI")
        print(data)

        update = telebot.types.Update.de_json(data)

        bot.process_new_updates([update])

        return "OK", 200

    except Exception as e:
        print("XATO:", e)
        return "ERROR", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
