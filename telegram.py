import os
import telebot
from flask import Flask, request


TOKEN = os.environ.get("TOKEN")
ADMIN_PHONE = "+998 99 434 10 00"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Webhook'ni darhol biriktirish
if WEBHOOK_URL:
    try:
        bot.remove_webhook()
        bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
        print(f"Webhook o'rnatildi: {WEBHOOK_URL}/webhook")
    except Exception as e:
        print(f"Webhook o'rnatishda xatolik: {e}")

@bot.message_handler(commands=["start"])
def start(message):
    text = f"""
🚘 Avtoraqam Andijon

Assalomu alaykum!

📞 Avtoraqam sotib olish yoki
ma'lumot olish uchun admin bilan bog'laning:

{ADMIN_PHONE}
"""
    bot.send_message(message.chat.id, text)

@app.route("/", methods=["GET"])
def home():
    return "Avtoraqam Andijon Bot ishlayapti!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    return "Forbidden", 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
