import os
from dotenv import load_dotenv
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import car_choices as cc
import keyboard as kb

user_states = {}

previous_message = {}

def update_message(update, context, text_to, reply_markup=None):
    if update.callback_query and update.callback_query.message:
        try:
            context.bot.edit_message_text(
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id,
                text=text_to,
                reply_markup=reply_markup,
                parse_mode="Markdown",  # You can specify the parse_mode here if needed
            )
        except Exception as e:
            print(f"Error updating message: {e}")
    else:
        # If the message doesn't exist, send a new one
        try:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=text_to,
                reply_markup=reply_markup,
                parse_mode="Markdown",  # You can specify the parse_mode here if needed
            )
        except Exception as e:
            print(f"Error sending message: {e}")

def cars(update: Update, context: CallbackContext):
    keyboard = kb.create_company_keyboard(cc.car_choices)
    update.message.reply_text("Please select a car company:", reply_markup=InlineKeyboardMarkup(keyboard))
    # Set the initial state to 'SELECT_COMPANY'
    user_states[update.message.chat_id] = 'SELECT_COMPANY'
    # Clear any previous messages
    if "chat_id" in previous_message:
        context.bot.delete_message(chat_id=previous_message["chat_id"], message_id=previous_message["message_id"])
def show_company_models(update, context):
    query = update.callback_query
    company_name = query.data.replace('show_company_', '')
    company_details = cc.car_choices.get(company_name)

    if company_details:
        model_info = f"Please select a car model from {company_name}:"
        keyboard = kb.create_model_keyboard(cc.car_choices, company_name)
        
        # Check if there's a previous message
        if "chat_id" in previous_message:
            # Update the existing message to avoid sending a new one
            query.edit_message_text(text=model_info, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            # Send the message as a new text message
            message = context.bot.send_message(chat_id=query.message.chat_id, text=model_info, reply_markup=InlineKeyboardMarkup(keyboard))
            # Store the message details in the previous_message dictionary
            previous_message["chat_id"] = query.message.chat_id
            previous_message["message_id"] = message.message_id
        
        # Update the user's state to 'SELECT_COMPANY'
        user_states[query.message.chat_id] = 'SELECT_COMPANY'
    else:
        query.answer(text="Company not found")


def show_model_description(update: Update, context: CallbackContext):
    query = update.callback_query
    _, company_name, model_name = query.data.split('_')[1:]
    company_details = cc.car_choices.get(company_name)

    if company_details and model_name in company_details["models"]:
        model_details = company_details["models"][model_name]
        description = model_details["description"]
        image_url = model_details["image_url"]
        year = model_details["year"]

        keyboard = kb.create_complete_set_keyboard(cc.car_choices, company_name, model_name)
        # Create a message with car information
        model_info = f"Model: {model_name}\nDescription: {description}\nYear: {year}\nPlease select a complete set:"

        # Store the current state in the user's context
        context.user_data["current_state"] = "SELECT_COMPLETE_SET"
        context.user_data["company_name"] = company_name
        context.user_data["model_name"] = model_name

        # Check if there's a previous message
        if "chat_id" in previous_message:
            # Update the existing message to avoid sending a new one
            query.edit_message_caption(caption=model_info, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            # Send the message as a new caption along with the car image
            message = context.bot.send_photo(chat_id=query.message.chat_id, photo=image_url, caption=model_info, reply_markup=InlineKeyboardMarkup(keyboard))
            # Store the message details in the previous_message dictionary
            previous_message["chat_id"] = query.message.chat_id
            previous_message["message_id"] = message.message_id
    else:
        query.answer(text="Model not found")

def show_complete_set_details(update: Update, context: CallbackContext):
    query = update.callback_query
    _, company_name, model_name, set_name = query.data.split('_')[1:]
    company_details = cc.car_choices.get(company_name)

    if company_details and model_name in company_details["models"]:
        model_details = company_details["models"][model_name]
        complete_sets = model_details.get("complete_sets")
        if complete_sets and set_name in complete_sets:
            set_details = complete_sets[set_name]
            description = set_details["description"]
            price = set_details["price"]

            set_info = f"Complete Set: {set_name}\nDescription: {description}\nPrice: {price}"

            # Store the current state in the user's context
            context.user_data["current_state"] = "SELECT_COMPLETE_SET_DETAILS"

            # Check if there's a previous message
            if "chat_id" in previous_message:
                # Update the existing message to avoid sending a new one
                query.edit_message_caption(caption=set_info)
                # You can also update the inline keyboard if needed
                keyboard = [[InlineKeyboardButton("Buy", callback_data=f"buy_{company_name}_{model_name}_{set_name}"),
                             InlineKeyboardButton("Go Back", callback_data=f"show_model_{company_name}_{model_name}")]]
                query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                query.answer(text="Previous message not found")
        else:
            query.answer(text="Complete set not found")


def go_back_to_models(update, context):
    chat_id = update.callback_query.message.chat_id
    current_state = user_states.get(chat_id)

    if current_state == 'SELECT_MODEL':
        # Go back to car companies selection
        keyboard = kb.create_company_keyboard(cc.car_choices)
        update_message(update, context, "Please select a car company:", InlineKeyboardMarkup(keyboard))
        user_states[chat_id] = 'SELECT_COMPANY'

        # Clear any previous messages
        if "chat_id" in previous_message:
            context.bot.delete_message(chat_id=previous_message["chat_id"], message_id=previous_message["message_id"])
    else:
        query = update.callback_query
        query.answer(text="Cannot go back in this context")

def go_back(update: Update, context: CallbackContext):
    # Retrieve the current state from the user's context
    current_state = context.user_data.get("current_state", "")
    chat_id = update.callback_query.message.chat_id

    # Implement logic to go back to the previous step based on the current_state
    if current_state == "SELECT_MODEL":
        # Handle going back from model selection to company selection
        cars(update, context)
        # Clear any previous messages
        if "chat_id" in previous_message:
            context.bot.delete_message(chat_id=previous_message["chat_id"], message_id=previous_message["message_id"])
    elif current_state == "SELECT_COMPLETE_SET":
        # Handle going back from complete set selection to model selection
        show_company_models(update, context)
        # Clear any previous messages
        if "chat_id" in previous_message:
            context.bot.delete_message(chat_id=previous_message["chat_id"], message_id=previous_message["message_id"])
    elif current_state == "SELECT_COMPLETE_SET_DETAILS":
        # Handle going back from complete set details to complete set selection
        show_complete_set_details(update, context)
    else:
        # Handle other cases or unknown states
        update.callback_query.answer(text="Cannot go back in this context")


def buy_complete_set(update: Update, context: CallbackContext):
    query = update.callback_query
    _, company_name, model_name, set_name = query.data.split('_')[1:]

    # Implement the logic for purchasing the complete set here
    # You can use the provided information to process the purchase

    query.answer(text=f"You have selected to buy the {set_name} complete set for {model_name} by {company_name}.")
