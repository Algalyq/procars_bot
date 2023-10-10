import logging
from dotenv import load_dotenv
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,CallbackContext, CommandHandler, CallbackQueryHandler,MessageHandler,Filters
from question import questions
from company import companies
import telebot 
from google.googleid import fetch_data
from telegram import InputMediaPhoto
from telegram import ChatAction


TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


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


def get_config_info(data_google, selected_company, selected_model, config_name):
    if selected_model == "001":
        selected_model = str(1)
    for row in data_google:
        if (
            row[0] == selected_company
            and row[1] == selected_model
            and row[2] == config_name
        ):
            return row
    return None

def generate_message_text(config_info):
    print(config_info)
    if config_info:
        description,vehicle_type, power, capacity, year, pw_reserve, torque, drive, max_speed, price_30, price_100, price_30_tg, price_100_tg = config_info[2:15]
        
        message_text = (
            f"Комплектация: {description}\n"
            f"Цена в $: При 30/70 оплате {price_30} (При 100% оплате {price_100})\n"
            f"Цена в ₸: При 30/70 оплате {price_30_tg} (При 100% оплате {price_100_tg})\n"
            f"Привод: {drive}\n"
            f"Мощность: {power}\n"
            f"{'Емкость батареи' if vehicle_type == 'Electro' else 'Объем двигателя'}: {capacity}\n"
            f"Максимальная скорость: {max_speed}\n"
            f"{'Запас хода' if vehicle_type == 'Electro' else 'Расход топлива в смешанном цикле'}: {pw_reserve}\n"
            f"{'Крутящий момент' if vehicle_type == 'Electro' else 'Объем топливного бака'}: {torque}\n"
            f"Наш номер: +7 700 807 92 92 \n"
        )
        return message_text
    return "Комплектация не найдена."

def choosed_car_model(config_info):

    if config_info:
        company,car,description,vehicle_type, power, capacity, year, pw_reserve, torque, drive, max_speed, price_30, price_100, price_30_tg, price_100_tg = config_info[0:15]
        message_text = (
            f"Вы выбрали: {company} {car} {description} \n"
        )
        
        return message_text
    return "Комплектация не найдена."

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
                context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
                if config_name in configurations:
                    config_info = get_config_info(data_google, selected_company, selected_model, config_name)
                    message_text = generate_message_text(config_info)
                    print(f"test: {config_name}")
                    message_text_2 = choosed_car_model(config_info)
                    image_url = config_info[15]
                    keyboard = [
                        [InlineKeyboardButton("Звонок от менеджера", callback_data=f'call_manager')],
                        [InlineKeyboardButton("Назад к моделям", callback_data=f'back_to_models')],
                        [InlineKeyboardButton("Назад к брендам", callback_data=f'back_to_companies')],
                    ]
                    media_group = []
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    if image_url:
                        image_urls_list = [url.strip() for url in image_url.split(',')]
                        for num, image_path in enumerate(image_urls_list):
                            media_group.append(InputMediaPhoto(image_path,caption = message_text if num == 0 else ''))
                        
                        query.delete_message()
 
                        context.bot.send_media_group(chat_id=query.message.chat_id, media=media_group)   
                        context.bot.send_message(chat_id=query.message.chat_id,text=message_text_2,reply_markup=reply_markup)
                         
                    else:
                        query.edit_message_text(text=message_text,reply_markup=reply_markup)
                else:
                    query.edit_message_text(text="Комплектация не найдена.")
            else:
                query.edit_message_text(text="Данные о комплектациях отсутствуют.")
        else:
            query.edit_message_text(text="Модель не найдена.")
    else:
        query.edit_message_text(text="Компания или модель не выбрана.")


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
