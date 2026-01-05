import os
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN belum diset di Environment Variables")

# ===== COMMANDS =====
def start(update, context):
    update.message.reply_text("🤖 Bot Setoran Aktif ✅")

def handle_text(update, context):
    text = update.message.text
    update.message.reply_text(f"📩 Pesan diterima:\n{text}")

# ===== MAIN =====
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    print("Bot sedang berjalan...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
