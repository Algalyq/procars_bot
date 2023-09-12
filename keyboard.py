# keyboards.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_company_keyboard(car_choices):
    keyboard = []
    for company_name in car_choices:
        keyboard.append([InlineKeyboardButton(company_name, callback_data=f"show_company_{company_name}")])
    return keyboard

def create_model_keyboard(car_choices, company_name):
    keyboard = []
    company_details = car_choices.get(company_name)
    if company_details:
        for model_name in company_details["models"]:
            keyboard.append([InlineKeyboardButton(model_name, callback_data=f"show_model_{company_name}_{model_name}")])

        # Add a "Go Back to Choose Companies" button
        keyboard.append([InlineKeyboardButton("Go Back to Choose Companies", callback_data=f"show_company_{company_name}")])
    return keyboard

def create_complete_set_keyboard(car_choices, company_name, model_name):
    keyboard = []
    company_details = car_choices.get(company_name)
    if company_details and model_name in company_details["models"]:
        model_details = company_details["models"][model_name]
        complete_sets = model_details.get("complete_sets")
        if complete_sets:
            for set_name in complete_sets:
                keyboard.append([InlineKeyboardButton(set_name, callback_data=f"show_set_{company_name}_{model_name}_{set_name}")])

            # Add a "Go Back" button to return to car models selection
            keyboard.append([InlineKeyboardButton("Go Back to Models", callback_data=f"show_company_{company_name}")])
    return keyboard
2