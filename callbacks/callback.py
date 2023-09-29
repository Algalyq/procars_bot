import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,MessageHandler,Filters
from question import questions
from company import companies
from google.googleid import fetch_data

from telegram import ChatAction


def callback_button(update, context):
    query = update.callback_query
    query.answer()

    data = query.data.split(':')
    company_name = data[1]

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

            keyboard = []

            for config_name in model_info.get("Комплектации", {}):
                keyboard.append([InlineKeyboardButton(config_name, callback_data=f'config:{config_name}')])

            keyboard.append([InlineKeyboardButton("Назад к моделям", callback_data=f'back_to_models')])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            message_text = f"Выбрана модель: {selected_company} {model_name}\n"

            query.edit_message_text(text=message_text, reply_markup=reply_markup)


def callback_call_manager(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Пожалуйста напишите /call чтобы оформить звонок от менеджера")

def callback_configuration(update, context):
    query = update.callback_query
    query.answer()

    data_google = fetch_data()
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
                    if selected_model == "001":
                        description = config_info.get("description")
                        for row in data_google:
                            if(row[0] == selected_company
                                and row[1] == str(int(selected_model))
                                and row[2] == description):
                                    print(row)
                                    power = row[4]
                                    capacity = row[5]
                                    year = row[6]
                                    pw_reserve = row[7]
                                    torque = row[8]
                                    drive = row[9]
                                    max_speed = row[10]
                                    price_30 = row[11]
                                    price_100 = row[12]
                                    price_30_tg = row[13]
                                    price_100_tg = row[14]
                                    message_text = (
                                            f"Комплектация: {description}\n"
                                            f"Цена в $: При 30/70 оплате {price_30} (При 100% оплате {price_100})\n"
                                            f"Цена в ₸: При 30/70 оплате {price_30_tg} (При 100% оплате {price_100_tg})\n"
                                            f"Привод: {drive}\n"
                                            f"Мощность: {power}\n"
                                            f"Емкость батареи: {capacity}\n"
                                            f"Максимальная скорость: {max_speed}\n"
                                            f"Запас хода: {pw_reserve} км\n"
                                            f"Крутящий момент: {torque}\n"
                                        )

                                    keyboard = [
                                        [InlineKeyboardButton("Звонок от менеджера", callback_data=f'call')],
                                        [InlineKeyboardButton("Назад к моделям", callback_data=f'back_to_models')],
                                        [InlineKeyboardButton("Назад к компаниям", callback_data=f'back_to_companies')],
                                    ]

                                    reply_markup = InlineKeyboardMarkup(keyboard)

                                    query.message.caption = message_text
                                    query.message.reply_markup = reply_markup
                                    query.edit_message_text(text=message_text, reply_markup=reply_markup)

                          


                    else: 
                        description = config_info.get("description")
                        for row in data_google:
                            if(row[0] == selected_company
                                and row[1] == selected_model
                                and row[2] == description and row[3] == "Electro"):
                                    print(row)
                                    power = row[4]
                                    capacity = row[5]
                                    year = row[6]
                                    pw_reserve = row[7]
                                    torque = row[8]
                                    drive = row[9]
                                    max_speed = row[10]
                                    price_30 = row[11]
                                    price_100 = row[12]
                                    price_30_tg = row[13]
                                    price_100_tg = row[14]
                                    message_text = (
                                            f"Комплектация: {description}\n"
                                            f"Цена в $: При 30/70 оплате {price_30} (При 100% оплате {price_100})\n"
                                            f"Цена в ₸: При 30/70 оплате {price_30_tg} (При 100% оплате {price_100_tg})\n"
                                            f"Привод: {drive}\n"
                                            f"Мощность: {power}\n"
                                            f"Емкость батареи: {capacity}\n"
                                            f"Максимальная скорость: {max_speed}\n"
                                            f"Запас хода: {pw_reserve} км\n"
                                            f"Крутящий момент: {torque}\n"
                                        )
                                    

                                    keyboard = [
                                        [InlineKeyboardButton("Звонок от менеджера", callback_data='call_manager')],
                                        [InlineKeyboardButton("Назад к моделям", callback_data=f'back_to_models')],
                                        [InlineKeyboardButton("Назад к компаниям", callback_data=f'back_to_companies')],
                                    ]

                                    reply_markup = InlineKeyboardMarkup(keyboard)

                                    query.message.caption = message_text
                                    query.message.reply_markup = reply_markup
                                    query.edit_message_text(text=message_text, reply_markup=reply_markup)

                            elif(row[0] == selected_company
                                and row[1] == selected_model
                                and row[2] == description and row[3] == "DVS"):
                                    print(row)
                                    power = row[4]
                                    capacity = row[5]
                                    year = row[6]
                                    pw_reserve = row[7]
                                    torque = row[8]
                                    drive = row[9]
                                    max_speed = row[10]
                                    price_30 = row[11]
                                    price_100 = row[12]
                                    price_30_tg = row[13]
                                    price_100_tg = row[14]
                                    message_text = (
                                            f"Комплектация: {description}\n"
                                            f"Цена в $: При 30/70 оплате {price_30} (При 100% оплате {price_100})\n"
                                            f"Цена в ₸: При 30/70 оплате {price_30_tg} (При 100% оплате {price_100_tg})\n"
                                            f"Привод: {drive}\n"
                                            f"Мощность: {power}\n"
                                            f"Объем двигателя: {capacity}\n"
                                            f"Максимальная скорость: {max_speed}\n"
                                            f"Расход топлива в смешанном цикле: {pw_reserve} \n"
                                            f"Объем топливного бака: {torque}\n"
                                        )

                                    keyboard = [
                                        [InlineKeyboardButton("Звонок от менеджера", callback_data=f'call')],
                                        [InlineKeyboardButton("Назад к моделям", callback_data=f'back_to_models')],
                                        [InlineKeyboardButton("Назад к компаниям", callback_data=f'back_to_companies')],
                                    ]

                                    reply_markup = InlineKeyboardMarkup(keyboard)

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

        new_text = 'Выберите модель автомобиля:'

        query.edit_message_text(
            text=new_text,
            reply_markup=reply_markup,
            parse_mode='Markdown')



def callback_companies(update, context):
    query = update.callback_query
    query.answer()

    keyboard = []

    for company in companies.keys():
        keyboard.append([InlineKeyboardButton(company, callback_data=f'company:{company}')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text='Выберите компанию:', reply_markup=reply_markup)
