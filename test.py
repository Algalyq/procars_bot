
import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask
from company import companies
from callbacks.callback import callback_button, callback_choose_model, callback_configuration, callback_models, callback_companies, callback_call_manager
from question import questions, call_manager, receive_username, receive_phone_number, verify_data, USERNAME, PHONE_NUMBER, VERIFY_DATA, handle_text_message
from gpt.bot import bot_answer
from datetime import date
import telebot
from google.googleid import fetch_data
import gspread
from strings import *

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot("6529806538:AAF2YQMDvb_vJBDlZRSVtGKsh08ihUdVjqI")
app = Flask(__name__)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
updater = Updater(token="6529806538:AAF2YQMDvb_vJBDlZRSVtGKsh08ihUdVjqI", use_context=True)
dispatcher = updater.dispatcher

scheduler = BackgroundScheduler()
scheduler.start()

# Initialize the user_data_dict
user_data_dict = {}

introduction_sent = {}

# Language selection constants
SELECT_LANGUAGE, CONFIRM_LANGUAGE = range(2)

# Supported languages
languages = {
    'en': 'English',
    'es': 'Spanish',
    # Add more languages here
}

# Function to start language selection
def start_language_selection(update, context):
    user = update.effective_user
    user_id = user.id
    user_data_dict[user_id] = {}  # Initialize user data for this user
    keyboard = []
    for language_code, language_name in languages.items():
        keyboard.append([InlineKeyboardButton(language_name, callback_data=f'language:{language_code}')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['user_id'] = user_id
    context.bot.send_message(user_id, "Select your preferred language:", reply_markup=reply_markup)
    return SELECT_LANGUAGE

# Function to handle language selection
def select_language(update, context):
    query = update.callback_query
    language_code = query.data.replace('language:', '')
    user_id = context.user_data['user_id']

    user_data_dict[user_id]['language'] = language_code

    query.answer()
    query.edit_message_text(f"Your language has been set to {languages[language_code]}")

    # You can customize the welcome message based on the selected language
    welcome_message = f"Welcome to the bot in {languages[language_code]}!"
    context.bot.send_message(user_id, welcome_message)

    return ConversationHandler.END

# Add command handler for starting language selection
dispatcher.add_handler(CommandHandler('language', start_language_selection))

# Add callback handler for language selection
dispatcher.add_handler(CallbackQueryHandler(select_language, pattern='^language:'))

# Define your other handlers (start, show_car_companies, etc.) as you had them

# Start the bot
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    import multiprocessing
    processes = [
        multiprocessing.Process(target=app.run, kwargs={'host': '0.0.0.0', 'port': port}),
        multiprocessing.Process(target=updater.start_polling),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
