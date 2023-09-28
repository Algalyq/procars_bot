import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,MessageHandler,Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask
from company import companies
from callbacks.callback import callback_button,callback_choose_model,callback_configuration,callback_models,callback_companies, callback_call_manager
from question import questions,call_manager,receive_username,receive_phone_number,verify_data,USERNAME,PHONE_NUMBER,VERIFY_DATA,handle_text_message
from gpt.bot import bot_answer
from datetime import date
import telebot 
from google.googleid import fetch_data
import gspread
from telegram.ext import ConversationHandler

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

scheduler = BackgroundScheduler()
scheduler.start()


user_data_dict = {}

introduction_sent = {}

def start(update, context):
    user = update.effective_user
    user_id = user.id
    if user_id not in introduction_sent:
        instructions = (
            f"Добро пожаловать в Profusion Cars!\n"
            "Я чат бот компаний Profusion Cars. Я помогу вам найти ответы на вопросы касаемо машины, комплектаций, цены и т.д.\n"
            "Вы можете задать вопрос в чат бот или через /questions посмотреть ответы на часто задаваемые вопросы \n\n"
            "Доступные команды:\n"
            "/questions - Показать это ответы на часто задаваемые вопросы\n"
            "/cars - Показать список машин и комплектаций, характеристики\n"
            "/call - Звонок от менеджера\n"
        )
        update.message.reply_html(instructions)
        introduction_sent[user_id] = True

def show_car_companies(update, context):
    keyboard = []
    


    for company in companies.keys():
        keyboard.append([InlineKeyboardButton(company, callback_data=f'company:{company}')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберите компанию:', reply_markup=reply_markup)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('cars', show_car_companies))
dispatcher.add_handler(CommandHandler('questions', questions))
dispatcher.add_handler(CallbackQueryHandler(callback_button, pattern='^company:'))
dispatcher.add_handler(CallbackQueryHandler(callback_choose_model, pattern='^model:'))
dispatcher.add_handler(CallbackQueryHandler(callback_configuration, pattern='^config:'))
dispatcher.add_handler(CallbackQueryHandler(callback_models, pattern='^back_to_models'))
dispatcher.add_handler(CallbackQueryHandler(callback_companies, pattern='^back_to_companies'))
conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('call', call_manager)],
        states={
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, receive_username)],
            PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, receive_phone_number)],
            VERIFY_DATA: [CallbackQueryHandler(verify_data)],
        },
        fallbacks=[]
    )
dispatcher.add_handler(conversation_handler)
dispatcher.add_handler(CallbackQueryHandler(callback_call_manager, pattern='^call_manager?'))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_message))

@app.route('/')
def index():
    return "Hello, World!"

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
