import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from company import companies
import os
from dotenv import load_dotenv
# Initialize OpenAI
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Create a bot instance
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()

# Установка уровня логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

user_data_dict = {}

introduction_sent = {}

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in introduction_sent:
        instructions = (
            f"Привет, {message.from_user.get_mention(as_html=True)}!\n"
            "Я чат бот компаний Profusion Cars. Я помогу вам найти ответы на вопросы касаемо машины, комплектаций, цены и т.д.\n"
            "Вы можете задать вопрос в чат бот или через /questions посмотреть ответы на часто задаваемые вопросы \n\n"
            "Доступные команды:\n"
            "/questions - Показать это ответы на часто задаваемые вопросы\n"
            "/cars - Показать список машин и комплектаций, характеристики\n"
            "/call - Звонок от менеджера\n"
        )
        await message.reply_html(instructions)
        introduction_sent[user_id] = True

@dp.message_handler(commands=['cars'])
async def show_car_companies(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for company in companies.keys():
        keyboard.add(types.InlineKeyboardButton(company, callback_data=f'company:{company}'))

    await message.reply('Выберите компанию:', reply_markup=keyboard)

@dp.message_handler(commands=['call'])
async def call_command(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, напишите ваш номер телефона. Например: +77081234567")

# Handle callback queries
@dp.callback_query_handler(lambda c: c.data.startswith('company:'))
async def callback_button(callback_query: types.CallbackQuery):
    await callback_query.message.answer(f'You pressed a button with callback data: {callback_query.data}')

# Your other callback handlers can go here

async def on_startup(dp):
    await bot.send_message(chat_id=991925952, text="Bot has been started")

async def on_shutdown(dp):
    await bot.send_message(chat_id=991925952, text="Bot has been stopped")

if __name__ == '__main__':
    from aiogram import executor
    from aiogram import types

    # Start the bot using the polling method
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
