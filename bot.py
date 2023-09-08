import os
from decouple import config
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Load the bot token from the .env file
TOKEN = config('TOKEN')

# Create a bot instance with the token
bot = telegram.Bot(token=TOKEN)

# Define a command handler
def start(update, context):
    update.message.reply_text('Hello! I am your Telegram bot.')

# Define a message handler
def echo(update, context):
    update.message.reply_text(update.message.text)

# Set up your conversation handler, if needed

# Create an updater
updater = Updater(bot=bot, use_context=True)

# Create a dispatcher for the handlers
dispatcher = updater.dispatcher

# Register your handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Start the bot
updater.start_polling()

# Run the bot until you stop it manually
updater.idle()
