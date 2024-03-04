from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import pyshorteners
from threading import Timer

# Replace 'YOUR_TELEGRAM_TOKEN' and 'YOUR_BITLY_TOKEN' with your actual tokens
TELEGRAM_TOKEN = '6438337961:AAG9YLEz6DXefnW_j_hr6oPSKaLOOWeDe2g'
BITLY_TOKEN = 'db8b6a1928c1a248ecfc7b9d26310d204f0d4193'

s = pyshorteners.Shortener(api_key=BITLY_TOKEN)

# Timer to refresh Bitly token every 24 hours (86400 seconds)
refresh_interval = 86400

def refresh_bitly_token():
    s.bitly.api_key = 'YOUR_NEW_BITLY_TOKEN'
    Timer(refresh_interval, refresh_bitly_token).start()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send me a link to shorten.')

def shorten_link(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    original_link = context.args[0]

    # Shorten the link using Bitly
    shortened_link = s.bitly.short(original_link)

    # Reply with the shortened link
    update.message.reply_text(f"Shortened link: {shortened_link}")

def main() -> None:
    # Initial Bitly token setup
    s.bitly.api_key = BITLY_TOKEN

    # Start the timer for token refresh
    Timer(refresh_interval, refresh_bitly_token).start()

    updater = Updater(token=TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("shorten", shorten_link, pass_args=True))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
  
