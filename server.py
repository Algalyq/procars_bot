import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from dotenv import load_dotenv
# Initialize OpenAI
# TOKEN = os.getenv("TOKEN")

TOKEN = "5907195764:AAF2QWHDtKSV30dJqKJsXKIlbQAr_hMGK9I"
# Create a Flask app
app = Flask(__name__)

# Set up logging for Flask
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set up the Telegram bot
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Set up the BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Your Telegram bot handlers go here
def start(update, context):
    update.message.reply_text("Hello! This is your Telegram bot.")

def echo(update, context):
    text = update.message.text
    update.message.reply_text(f"You said: {text}")

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Your Flask routes go here
@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    # Run the Flask app and the Telegram bot updater using gunicorn
    port = int(os.environ.get('PORT', 5000))

    # Start the Flask app and Telegram bot updater as separate processes
    import multiprocessing
    processes = [
        multiprocessing.Process(target=app.run, kwargs={'host': '0.0.0.0', 'port': port}),
        multiprocessing.Process(target=updater.start_polling),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
