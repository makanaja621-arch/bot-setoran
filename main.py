import os
import re
import gspread
from telegram.ext import Updater, MessageHandler, Filters
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = os.getenv("8216179180:AAFGtV2v4qKw82_QC8sxnG763qBDZ_zhi38")
SHEET_NAME = os.getenv("Setoran Video")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = {
    "type": "service_account",
    "project_id": os.getenv("GCP_PROJECT_ID"),
    "private_key_id": os.getenv("GCP_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GCP_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("GCP_CLIENT_EMAIL"),
    "client_id": os.getenv("GCP_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv("GCP_CERT_URL")
}

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

def handle_video(update, context):
    if not update.message.video:
        return

    caption = update.message.caption or ""
    match = re.search(r"(\d+)", caption)
    point = int(match.group(1)) if match else 1

    username = update.message.from_user.username or update.message.from_user.first_name
    sheet.append_row([username, point])

    update.message.reply_text(f"{username}\n{point}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.video, handle_video))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()


