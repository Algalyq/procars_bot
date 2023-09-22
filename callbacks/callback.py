import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,MessageHandler,Filters
from question import questions,answer_question
from company import companies



# Обработчик для кнопок выбора компании
def callback_button(update, context):
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
        


def callback_choose_model(update, context):
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



def callback_call(update, context):
    query = update.callback_query
    user = update.effective_user
    user_id = user.id
    query.edit_message_text(text=f"{user.first_name}, напишите ваш номер телефон. Например: +77081234567")

def callback_configuration(update, context):
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
                    Обьем = config_info.get("Обьем")
                    # Determine car type (electric or oil) based on some criteria in your data
                    car_type = model_info['Тип двигателя']  # Replace with your logic to determine car type
                    mileage = config_info.get("mileage")
                    if car_type == "Электрический":
                        # Customize information for electric cars
                        electric_info = config_info.get("electric_info")
                        message_text = (
                            f"Комплектация: {description}\n"
                            f"Цена: {price}\n"
                            f"Привод: {drive}\n"
                            f"Мощность: {power}\n"
                            f"Емкость батареи: {capacity}\n"
                            f"Максимальная скорость: {max_speed}\n"
                            f"Запас хода: {mileage}\n"
                            f"Крутящий момент: {torque}\n"
                            f"Дополнительная информация для электрических машин: {electric_info}\n"
                        )
                    else:
                        # Customize information for oil cars (internal combustion engine)
                        oil_info = config_info.get("oil_info")
                        message_text = (
                            f"Цена: {price}\n"
                            f"Привод: {drive}\n"
                            f"Мощность: {power}\n"
                            f"Расход: {capacity}\n"
                            f"Максимальная скорость: {max_speed}\n"
                            f"Крутящий момент: {torque}\n"
                            
                            f"Обьем: {Обьем}\n"
                            f"Комплектация: {description}\n"
                          )

                    keyboard = [
                        [InlineKeyboardButton("Звонок от менеджера", callback_data=f'call')],
                        [InlineKeyboardButton("Назад к моделям", callback_data=f'back_to_models')],
                        [InlineKeyboardButton("Назад к компаниям", callback_data=f'back_to_companies')],
                    ]

                    reply_markup = InlineKeyboardMarkup(keyboard)

                    # Update the existing message's caption with new information
                    query.message.caption = message_text
                    query.message.reply_markup = reply_markup
                    query.edit_message_text(text=message_text, reply_markup=reply_markup)


def callback_models(update, context):
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
def callback_companies(update, context):
    query = update.callback_query
    query.answer()

    keyboard = []

    for company in companies.keys():
        keyboard.append([InlineKeyboardButton(company, callback_data=f'company:{company}')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Clear the caption, photo, and set the updated reply markup for the message
    query.edit_message_text(text='Выберите компанию:', reply_markup=reply_markup)
