import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,MessageHandler,Filters
from test import questions,answer_question
import bot2 as bot
# Замените 'YOUR_BOT_TOKEN' на ваш токен
TOKEN = "5907195764:AAENObL59xrfDu8HYgNDWkQf9dX0l43S0xw"

# Установка уровня логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создание обновления и диспетчера
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Словарь компаний, где ключ - название компании, значение - список моделей
companies = {
   "Honda": {
        "Honda eNS1": {
            "Год выпуска": 2022,
            "Характеристики": "Honda e:NS1",
            "Фото": "https://static.tildacdn.com/stor6436-3264-4432-b764-366463343961/32280260.jpg",
            "Комплектации": {
                "Базовая комплектация": {
                    "description": "Базовая комплектация",
                    "price": "$9,000,000 (при 100% оплате будет $8,200,000)",
                    "mileage": "-",
                    "drive": "Полный",
                    "power": "134kW (182 л.с.)",
                    "capacity": "53.6 кВт*ч",
                    #added fields
                    "max_speed": "150 км/ч",
                    "torque": "310 н.м",
                    "push_start": "✅", 
                    # 
                },
                "Полная комплектация": {
                    "description": "Полная комплектация",
                    "price": "$11,000,000 (при 100% оплате будет $10,200,000)",
                    "mileage": "-",
                    "drive": "Полный",
                    "power": "150kW (204 л.с.)",
                    "capacity": "68.8 кВт*ч",
                    "max_speed": "150 км/ч",
                    "torque": "310 н.м",
                    "push_start": "✅", 
                },
            },
        },
        "Honda eNP1": {
            "Год выпуска": 2022,
            "Характеристики": "Honda e:NP1",
            "Фото": "https://static.tildacdn.com/stor6436-3264-4432-b764-366463343961/32280260.jpg",
            "Комплектации": {
                "Базовая комплектация": {
                    "description": "Базовая комплектация",
                    "price": "$9,000,000",
                    "mileage": "-",
                    "drive": "Полный",
                    "power": "134kW",
                    "capacity": "53.6 кВт*ч",
                    "max_speed": "150 км/ч",
                    "torque": "310 н.м",
                    "push_start": "✅", 
                },
                "Полная комплектация": {
                    "description": "Полная комплектация",
                    "price": "$11,000,000 (при 100% оплате будет $10,200,000)",
                    "mileage": "-",
                    "drive": "Полный",
                    "power": "150kW",
                    "capacity": "68.8 кВт*ч",
                    "max_speed": "150 км/ч",
                    "torque": "310 н.м",
                    "push_start": "✅",
                },
            },
        },
    },
    "Zeekr": {
        "Zeekr 001": {
            "Год выпуска": 2023,
            "Характеристики": "Zeekr 001",
            "Фото":     "https://static.tildacdn.com/stor6436-3264-4432-b764-366463343961/32280260.jpg",
            "Комплектации": {
                "WE": {
                    "description": "Описание",
                    "price": "$44000 - 45000",
                    "mileage": "",
                    "drive": "Полный",
                    "power": "400kW",
                    "capacity": "86,0 кВт*ч",
                    "max_speed": "150 км/ч",
                    "torque": "768 н.м",
                    "push_start": "✅",
                    
                },
                "Комплектация 2.1.2": {
                    "description": "Описание 2.1.2",
                    "price": "$58 000",
                    "mileage": "750km",
                    "drive": "Задний",
                    "power": "320kW",
                    "capacity": "85kWh",
                    "max_speed": "150 км/ч",
                    "torque": "310 н.м",
                    "push_start": "✅",
                },
            },
        },
        "Zeekr X": {
            "Год выпуска": 2022,
            "Характеристики": "Характеристики модели 2.2",
            "Фото":     "https://static.tildacdn.com/stor6436-3264-4432-b764-366463343961/32280260.jpg",
            "Комплектации": {
                "Комплектация 2.2.1": {
                    "description": "Описание 2.2.1",
                    "price": "$48 000",
                    "mileage": "550km",
                    "drive": "Полный",
                    "power": "350kW",
                    "capacity": "90kWh",
                    "max_speed": "150 км/ч",
                    "torque": "310 н.м",
                    "push_start": "✅",
                },
                "Комплектация 2.2.2": {
                    "description": "Описание 2.2.2",
                    "price": "$52 000",
                    "mileage": "600km",
                    "drive": "Задний",
                    "power": "300kW",
                    "capacity": "80kWh",
                    "max_speed": "150 км/ч",
                    "torque": "310 н.м",
                    "push_start": "✅",
                },
            },
        },
    },
}

introduction_sent = {}

# Обработчик команды /start
def start(update, context):
    user = update.effective_user
    user_id = user.id
    if user_id not in introduction_sent:
        instructions = (
            f"Привет, {user.mention_html()}!\n"
            "Я чат бот компаний Profusion Cars. Я помогу вам найти ответы на вопросы касаемо машины, комплектаций, цены и т.д.\n"
            "Вы можете задать вопрос в чат бот или через /questions посмотреть ответы на часто задаваемые вопросы \n\n"
            "Доступные команды:\n"
            "/questions - Показать это ответы на часто задаваемые вопросы\n"
            "/cars - Показать список машин и комплектаций, характеристики\n"
        )
        update.message.reply_html(instructions)
        introduction_sent[user_id] = True
    # instructions = (
    #         f"Привет, {user.mention_html()}!\n"
    #         "Я чат бот компаний Profusion Cars. Я помогу вам найти ответы на вопросы касаемо машины, комплектаций, цены и т.д.\n"
    #         "Вы можете задать вопрос в чат бот или через /questions посмотреть ответы на часто задаваемые вопросы \n\n"
    #         "Доступные команды:\n"
    #         "/questions - Показать это ответы на часто задаваемые вопросы\n"
    #         "/cars - Показать список машин и комплектаций, характеристики\n"
    #     )
    # user = update.effective_user
    # context.bot.send_message(chat_id=update.effective_chat.id,
    #                          text=f"Привет, {user.mention_html()}! Добро пожаловать в бота по автомобилям. "
    #                               f"Нажмите /cars, чтобы начать.")

# Обработчик команды /cars
def show_car_companies(update, context):
    keyboard = []

    for company in companies.keys():
        keyboard.append([InlineKeyboardButton(company, callback_data=f'company:{company}')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберите компанию:', reply_markup=reply_markup)

# Обработчик для кнопок выбора компании
def button(update, context):
    query = update.callback_query
    query.answer()

    data = query.data.split(':')
    company_name = data[1]

    # Сохраняем выбранную компанию в контексте пользователя
    context.user_data["selected_company"] = company_name

    if company_name in companies:
        models_for_company = companies[company_name]
        keyboard = []

        for model_name in models_for_company.keys():
            keyboard.append([InlineKeyboardButton(model_name, callback_data=f'model:{model_name}')])

        keyboard.append([InlineKeyboardButton("Назад", callback_data=f'back_to_companies')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        text=f"Выбрана компания: {company_name}\nВыберите модель автомобиля:"
        query.edit_message_text(text=f"Выбрана компания: {company_name}\nВыберите модель автомобиля:", reply_markup=reply_markup)
        

def choose_model(update, context):
    query = update.callback_query
    query.answer()

    data = query.data.split(':')
    model_name = data[1]

    selected_company = context.user_data.get("selected_company")
    if selected_company and selected_company in companies:
        models_for_company = companies[selected_company]
        if model_name in models_for_company:
            context.user_data["selected_model"] = model_name
            model_info = models_for_company[model_name]
            model_photo = model_info["Фото"]
            model_year = model_info["Год выпуска"]
            model_characteristics = model_info["Характеристики"]

            keyboard = []

            # Добавляем кнопки выбора комплектации для выбранной модели
            for config_name in model_info.get("Комплектации", {}):
                keyboard.append([InlineKeyboardButton(config_name, callback_data=f'config:{config_name}')])

            keyboard.append([InlineKeyboardButton("Назад к моделям", callback_data=f'back_to_models')])
            reply_markup = InlineKeyboardMarkup(keyboard)

            message_text = f"Выбрана модель: {model_name}\nГод выпуска: {model_year}\nХарактеристики: {model_characteristics}"

            # Отправляем фотографию и текст сообщения
            # context.bot.send_photo(chat_id=update.effective_chat.id, photo=model_photo, caption=message_text,
            #                        reply_markup=reply_markup)
            query.edit_message_text(text=message_text, reply_markup=reply_markup)
# ...


# Обработчик для кнопок выбора комплектации
def choose_configuration(update, context):
    query = update.callback_query
    query.answer()

    data = query.data.split(':')
    config_name = data[1]

    selected_model = context.user_data.get("selected_model")
    selected_company = context.user_data.get("selected_company")

    if selected_company and selected_company in companies and selected_model:
        models_for_company = companies[selected_company]
        if selected_model in models_for_company:
            model_info = models_for_company[selected_model]

            if "Комплектации" in model_info:
                configurations = model_info["Комплектации"]
                if config_name in configurations:
                    config_info = configurations[config_name]

                    description = config_info.get("description")
                    price = config_info.get("price")
                    drive = config_info.get("drive")
                    power = config_info.get("power")
                    capacity = config_info.get("capacity")
                    max_speed = config_info.get("max_speed")
                    torque = config_info.get("torque")
                    push_start = config_info.get("push_start")
                    message_text = (
                        f"Комплектация: {description}\n"
                        f"Цена: {price}\n"
                        f"Привод: {drive}\n"
                        f"Мощность: {power}\n"
                        f"Емкость батареи: {capacity}\n"
                        f"Максимальная скорость: {max_speed}\n"
                        f"Крутящий момент: {torque}\n"
                        f"Кнопка запуска: {push_start}\n"
                    )

                    keyboard = [
                        [InlineKeyboardButton("Назад к моделям", callback_data=f'back_to_models')],
                        [InlineKeyboardButton("Назад к компаниям", callback_data=f'back_to_companies')],
                    ]

                    if config_name != "Complete Car":  # Check if it's not the "Complete Car" option
                        keyboard.append([InlineKeyboardButton("Complete Car", callback_data=f'config:Complete Car')])

                    reply_markup = InlineKeyboardMarkup(keyboard)

                    # Update the existing message's caption with new information
                    query.message.caption = message_text
                    query.message.reply_markup = reply_markup
                    query.edit_message_text(text=message_text, reply_markup=reply_markup)

def back_to_models(update, context):
    query = update.callback_query
    query.answer()

    selected_company = context.user_data.get("selected_company")

    if selected_company and selected_company in companies:
        models_for_company = companies[selected_company]
        keyboard = []

        for model_name in models_for_company.keys():
            keyboard.append([InlineKeyboardButton(model_name, callback_data=f'model:{model_name}')])

        keyboard.append([InlineKeyboardButton("Назад к компаниям", callback_data=f'back_to_companies')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Define the new text you want for the message
        new_text = 'Выберите модель автомобиля:'

        # Use the edit_message_text method to update the text and reply_markup
        query.edit_message_text(
            text=new_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'  # You can specify the parsing mode if needed
        )


# Обработчик для кнопки "Назад" от компании к списку компаний
def back_to_companies(update, context):
    query = update.callback_query
    query.answer()

    keyboard = []

    for company in companies.keys():
        keyboard.append([InlineKeyboardButton(company, callback_data=f'company:{company}')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Clear the caption, photo, and set the updated reply markup for the message
    query.edit_message_text(text='Выберите компанию:', reply_markup=reply_markup)

# Регистрация обработчиков
start_handler = CommandHandler('start', start)
cars_handler = CommandHandler('cars', show_car_companies)
dispatcher.add_handler(CommandHandler('questions', questions))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer_question))
dispatcher.add_handler(start_handler)
dispatcher.add_handler(cars_handler)
dispatcher.add_handler(CallbackQueryHandler(button, pattern='^company:'))
dispatcher.add_handler(CallbackQueryHandler(choose_model, pattern='^model:'))
dispatcher.add_handler(CallbackQueryHandler(choose_configuration, pattern='^config:'))
dispatcher.add_handler(CallbackQueryHandler(back_to_models, pattern='^back_to_models'))
dispatcher.add_handler(CallbackQueryHandler(back_to_companies, pattern='^back_to_companies'))

# Запуск бота
updater.start_polling()

# Завершение бота при получении сигнала Ctrl+C
updater.idle()
