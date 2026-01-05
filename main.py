import os
import json
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEET_NAME = os.getenv("SHEET_NAME")

bot = Bot(token=BOT_TOKEN)

# ===== FLASK =====
app = Flask(__name__)

# ===== GOOGLE SHEET AUTH =====
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# ===== DISPATCHER =====
dispatcher = Dispatcher(bot, None, workers=0)

def start(update, context):
    update.message.reply_text("Bot Setoran Aktif ✅")

def handle_text(update, context):
    text = update.message.text
    update.message.reply_text(f"Pesan diterima:\n{text}")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

# ===== WEBHOOK =====
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# ===== RUN =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
