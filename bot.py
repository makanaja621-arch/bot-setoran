from telegram.ext import Updater, MessageHandler, Filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

TOKEN = os.getenv("BOT_TOKEN")
SHEET_NAME = os.getenv("SHEET_NAME")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1


def handle_video(update, context):
    msg = update.message

    if not msg.video or not msg.caption:
        return

    username = msg.from_user.username
    point = msg.caption.strip()

    if not username:
        msg.reply_text("❌ Username Telegram wajib aktif")
        return

    if not point.isdigit():
        msg.reply_text("❌ Caption harus ANGKA saja\nContoh: 88")
        return

    headers = sheet.row_values(1)

    if username not in headers:
        msg.reply_text(f"❌ Username @{username} tidak ada di sheet")
        return

    col = headers.index(username) + 1
    col_values = sheet.col_values(col)
    next_row = len(col_values) + 1

    sheet.update_cell(next_row, col, point)

    msg.reply_text(
        f"✅ Setoran diterima\n"
        f"👤 @{username}\n"
        f"⭐ Point: {point}"
    )


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(
        MessageHandler(Filters.video & Filters.caption, handle_video)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
