import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gpt.bot import bot_answer as bot 
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import request as req
from validator import validation
from telegram.ext import ConversationHandler
from telegram import ChatAction
import re
from google.googleid import fetch_data_question
from request import send_data_to_api
import time
from strings import *

# Define conversation states for the FSM
USERNAME, PHONE_NUMBER, VERIFY_DATA = range(3)


# Функция для команды /start
def questions(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        text=answer_to_question,
        reply_markup=get_questions_keyboard(),
    )

def get_questions_keyboard():
    keyboard = []
    for question in fetch_data_question().keys():
        keyboard.append([question])
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

def call_manager(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(input_name)
    return USERNAME

# Function to handle the username input
def receive_username(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data['username'] = update.message.text
    update.message.reply_text(input_phone_number)
    return PHONE_NUMBER


# Function to handle the phone number input
def receive_phone_number(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    phone_number = update.message.text.strip()  # Remove leading/trailing spaces

    # Define a regular expression pattern to match a valid phone number format
    phone_number_pattern = r'^\+?\d{11,12}$'  # Modify the pattern as needed

    if re.match(phone_number_pattern, phone_number):
        user_data['phone_number'] = phone_number

        # Create a custom keyboard with "Yes" and "No" buttons to verify data
        keyboard = [
            [InlineKeyboardButton("Да", callback_data='yes')],
            [InlineKeyboardButton("Нет", callback_data='no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            check_data(user_data['username'], user_data['phone_number']),
            reply_markup=reply_markup,
        )
        return VERIFY_DATA
    else:
        update.message.reply_text(input_correct_phone_number)
        return PHONE_NUMBER


def verify_data(update, context):
    query = update.callback_query
    user_data = context.user_data

    if query.data == 'yes':
        # Data is correct, set the 'verified' flag to True
        user_data['verified'] = True
        send_data_to_api(user_data['username'],user_data['phone_number'])
        query.edit_message_text(text=manager_call)
    elif query.data == 'no':
        query.edit_message_text(text=call_command_text)
        return ConversationHandler.END

def handle_text_message(update, context):
    user_message = update.message.text

    if context.user_data.get('verified', True):
        # If the user's data is verified, check if the message is a question
        if user_message in fetch_data_question().keys():
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
            answer = fetch_data_question().get(user_message)
            update.message.reply_text(answer)
        else:
            # If not a question, proceed with ChatGPT interactions
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
            chatgpt_response = bot(user_message)  # Use your ChatGPT function here
            update.message.reply_text(chatgpt_response)
    else:
        # If the user's data is not verified, you can handle other interactions here
        update.message.reply_text(verify_data)
