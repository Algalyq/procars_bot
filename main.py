import os
from dotenv import load_dotenv
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler


# Load environment variables from .env file
load_dotenv()

# Define your Telegram bot token
TOKEN = os.getenv("tg_token")

# Create an Updater object
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Initialize OpenAI
openai.api_key = os.getenv("ai_token")

# Define a dictionary to store car choices and their details
car_choices = {
    "Zeekr": {
        "models": {
            "0001": {
                "description": "Description for Model A1",
                "image_url": "https://static.tildacdn.com/stor6436-3264-4432-b764-366463343961/32280260.jpg",
                "year": "Year for Model A1",
                "complete_sets": {
                    "You": {
                        "description": "Complete Set A1.1 Description",
                        "price": "$XX,XXX",
                    },
                    "Me": {
                        "description": "Complete Set A1.2 Description",
                        "price": "$XX,XXX",
                    },
                },
            },
            # ... (other models)
        },
    },
    # ... (other companies)
}

previous_message = {}
# Create an inline keyboard with car companies
def create_company_keyboard():
    keyboard = []
    for company_name in car_choices:
        keyboard.append([InlineKeyboardButton(company_name, callback_data=f"show_company_{company_name}")])
    return keyboard

# Create an inline keyboard with car models for a selected company
def create_model_keyboard(company_name):
    keyboard = []
    company_details = car_choices.get(company_name)
    if company_details:
        for model_name in company_details["models"]:
            keyboard.append([InlineKeyboardButton(model_name, callback_data=f"show_model_{company_name}_{model_name}")])
    return keyboard

# Create an inline keyboard with complete sets for a selected model
def create_complete_set_keyboard(company_name, model_name):
    keyboard = []
    company_details = car_choices.get(company_name)
    if company_details and model_name in company_details["models"]:
        model_details = company_details["models"][model_name]
        complete_sets = model_details.get("complete_sets")
        if complete_sets:
            for set_name in complete_sets:
                keyboard.append([InlineKeyboardButton(set_name, callback_data=f"show_set_{company_name}_{model_name}_{set_name}")])
    keyboard.append([InlineKeyboardButton("Go Back", callback_data=f"show_company_{company_name}")])
    return keyboard

# Define a dictionary to store user states
user_states = {}

def start(update: Update, context: CallbackContext):
    keyboard = create_company_keyboard()
    update.message.reply_text("Please select a car company:", reply_markup=InlineKeyboardMarkup(keyboard))
    # Set the initial state to 'SELECT_COMPANY'
    user_states[update.message.chat_id] = 'SELECT_COMPANY'
def update_message(update: Update, context: CallbackContext, text_to: str, reply_markup=None):
    query = update.callback_query

    if query.message:
        try:
            context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
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
                chat_id=query.from_user.id,
                text=text_to,
                reply_markup=reply_markup,
                parse_mode="Markdown",  # You can specify the parse_mode here if needed
            )
        except Exception as e:
            print(f"Error sending message: {e}")


def show_company_models(update: Update, context: CallbackContext):
    query = update.callback_query
    company_name = query.data.replace('show_company_', '')
    company_details = car_choices.get(company_name)

    if company_details:
        keyboard = create_model_keyboard(company_name)
        update_message(update, context, f"Please select a car model from {company_name}:", InlineKeyboardMarkup(keyboard))
        # Update the user's state to 'SELECT_MODEL'
        user_states[query.message.chat_id] = 'SELECT_MODEL'
    else:
        query.answer(text="Company not found")


def show_model_description(update: Update, context: CallbackContext):
    query = update.callback_query
    print(query.data)
    _, company_name, model_name = query.data.split('_')[1:]
    company_details = car_choices.get(company_name)

    if company_details and model_name in company_details["models"]:
        model_details = company_details["models"][model_name]
        description = model_details["description"]
        image_url = model_details["image_url"]
        year = model_details["year"]

        keyboard = create_complete_set_keyboard(company_name, model_name)
        # Create a message with car information
        model_info = f"Model: {model_name}\nDescription: {description}\nYear: {year}\nPlease select a complete set:"

        # Check if there's a previous message
        if "chat_id" in previous_message:
            # Update the existing message to avoid sending a new one
            query.edit_message_caption(caption=model_info)
            q
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
    company_details = car_choices.get(company_name)

    if company_details and model_name in company_details["models"]:
        model_details = company_details["models"][model_name]
        complete_sets = model_details.get("complete_sets")
        if complete_sets and set_name in complete_sets:
            set_details = complete_sets[set_name]
            description = set_details["description"]
            price = set_details["price"]

            set_info = f"Complete Set: {set_name}\nDescription: {description}\nPrice: {price}"

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
# This code keeps track of the previous message's details in the previous_message dictionary and updates the existing message when the "Go Back" button is pressed, avoiding the need to send a new message.






def gpt(update: Update, context: CallbackContext):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant for Profusion Cars, and you will only answer questions about the company."},
            {"role": "user", "content": update.message.text},
        ],
    )
    update.message.reply_text(response.choices[0].message["content"])

# Register handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(show_company_models, pattern=r'show_company_'))
dispatcher.add_handler(CallbackQueryHandler(show_model_description, pattern=r'show_model_'))
dispatcher.add_handler(CallbackQueryHandler(show_complete_set_details, pattern=r'show_set_'))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, gpt))

if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
