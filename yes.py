import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Замените 'YOUR_BOT_TOKEN' на ваш токен
TOKEN = "5907195764:AAENObL59xrfDu8HYgNDWkQf9dX0l43S0xw"

# Установка уровня логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создание обновления и диспетчера
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Словарь компаний, где ключ - название компании, значение - список моделей
companies = {
    "Компания 1": {
        "Модель 1.1": {
            "Год выпуска": 2023,
            "Характеристики": "Характеристики модели 1.1",
            "Фото": "https://example.com/model1.jpg",
            "Комплектации": {
                "Комплектация 1.1.1": {
                    "description": "Описание 1.1.1",
                    "price": "$56 700",
                    "mileage": "650km",
                    "drive": "Полный",
                    "power": "400kW",
                    "capacity": "100kWh",
                },
                "Комплектация 1.1.2": {
                    "description": "Описание 1.1.2",
                    "price": "$60 000",
                    "mileage": "800km",
                    "drive": "Задний",
                    "power": "350kW",
                    "capacity": "90kWh",
                },
            },
        },
        "Модель 1.2": {
            "Год выпуска": 2022,
            "Характеристики": "Характеристики модели 1.2",
            "Фото": "https://example.com/model2.jpg",
            "Комплектации": {
                "Комплектация 1.2.1": {
                    "description": "Описание 1.2.1",
                    "price": "$45 000",
                    "mileage": "500km",
                    "drive": "Полный",
                    "power": "300kW",
                    "capacity": "80kWh",
                },
                "Комплектация 1.2.2": {
                    "description": "Описание 1.2.2",
                    "price": "$50 000",
                    "mileage": "600km",
                    "drive": "Задний",
                    "power": "250kW",
                    "capacity": "70kWh",
                },
            },
        },
    },
    "Компания 2": {
        "Модель 2.1": {
            "Год выпуска": 2023,
            "Характеристики": "Характеристики модели 2.1",
            "Фото": "https://example.com/model3.jpg",
            "Комплектации": {
                "Комплектация 2.1.1": {
                    "description": "Описание 2.1.1",
                    "price": "$55 000",
                    "mileage": "700km",
                    "drive": "Полный",
                    "power": "380kW",
                    "capacity": "95kWh",
                },
                "Комплектация 2.1.2": {
                    "description": "Описание 2.1.2",
                    "price": "$58 000",
                    "mileage": "750km",
                    "drive": "Задний",
                    "power": "320kW",
                    "capacity": "85kWh",
                },
            },
        },
        "Модель 2.2": {
            "Год выпуска": 2022,
            "Характеристики": "Характеристики модели 2.2",
            "Фото": "https://example.com/model4.jpg",
            "Комплектации": {
                "Комплектация 2.2.1": {
                    "description": "Описание 2.2.1",
                    "price": "$48 000",
                    "mileage": "550km",
                    "drive": "Полный",
                    "power": "350kW",
                    "capacity": "90kWh",
                },
                "Комплектация 2.2.2": {
                    "description": "Описание 2.2.2",
                    "price": "$52 000",
                    "mileage": "600km",
                    "drive": "Задний",
                    "power": "300kW",
                    "capacity": "80kWh",
                },
            },
        },
    },
}

# Обработчик команды /start
def start(update, context):
    user = update.effective_user
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Привет, {user.mention_html()}! Добро пожаловать в бота по автомобилям. "
                                  f"Нажмите /cars, чтобы начать.")

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

        query.edit_message_text(text=f"Выбрана компания: {company_name}\nВыберите модель автомобиля:", reply_markup=reply_markup)

# Обработчик для кнопок выбора модели
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

            query.edit_message_text(text=message_text, reply_markup=reply_markup)

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
                    mileage = config_info.get("mileage")
                    drive = config_info.get("drive")
                    power = config_info.get("power")
                    capacity = config_info.get("capacity")

                    message_text = (
                        f"Комплектация: {description}\n"
                        f"Цена: {price}\n"
                        f"Пробег: {mileage}\n"
                        f"Привод: {drive}\n"
                        f"Мощность: {power}\n"
                        f"Емкость батареи: {capacity}"
                    )

                    keyboard = [
                        [InlineKeyboardButton("Назад к моделям", callback_data=f'back_to_models')],
                        [InlineKeyboardButton("Назад к компаниям", callback_data=f'back_to_companies')],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)

                    query.edit_message_text(text=message_text, reply_markup=reply_markup)

# Обработчик для кнопки "Назад" от модели к списку моделей
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

        query.edit_message_text(text=f"Выберите модель автомобиля:", reply_markup=reply_markup)

# Обработчик для кнопки "Назад" от компании к списку компаний
def back_to_companies(update, context):
    query = update.callback_query
    query.answer()

    keyboard = []

    for company in companies.keys():
        keyboard.append([InlineKeyboardButton(company, callback_data=f'company:{company}')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text='Выберите компанию:', reply_markup=reply_markup)

# Регистрация обработчиков
start_handler = CommandHandler('start', start)
cars_handler = CommandHandler('cars', show_car_companies)
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
