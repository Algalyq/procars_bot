import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gpt.bot import bot_answer as bot 
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import request as req
from validator import validation
from telegram.ext import ConversationHandler



# Define conversation states for the FSM
USERNAME, PHONE_NUMBER, VERIFY_DATA = range(3)

# Список вопросов и ответов
questions_answers = {
    "Какие способы оплаты предоставляются для приобретения автомобиля?": " У нас есть два варианта оплаты. Вы можете выбрать оплату в размере 30% при подписании договора и оставшиеся 70% после доставки машины в Казахстан. Также доступна оплата на 100%, в этом случае вы оплачиваете всю стоимость машины, и мы сделаем вам скидку.",
    "Сколько времени занимает доставка автомобиля до границы Казахстана (Хоргос)?": "Доставка автомобиля до Хоргоса занимает обычно 10-15 дней. Важно учесть, что большую часть времени машина может стоять в очереди на границе. Суммарный срок ожидания машины составляет 35 дней с момента подписания договора и до доставки в Алматы.",
    "Что подразумевается под доставкой под ключ?": "Мы берем на себя все заботы по машине. Это включает в себя доставку машины из Китая, растаможку, уплату утилизационного сбора и оформление автомобиля на казахстанский учет. Вам нужно только приехать и забрать свою машину, которая уже будет с казахстанскими номерами.",
    "Как узнать о наличии машины для просмотра?": "Вы можете написать /call, и мы свяжемся с вами для уточнения наличия машины, которую вы хотели бы посмотреть.Но нужно учесть что мы не дилеры, а офис. Поэтому у нас нет машин на выставке. Мы можем показать вам машину, которая находится в офисе, но для этого нужно согласовать время и дату.",
    "Какие мировые производители электрических автомобилей представлены в вашем каталоге?": "В нашем каталоге представлены электрические автомобили от ведущих мировых производителей, таких как Zeekr, Volkswagen, Tesla, BYD, BMW, Toyota, Honda и Mazda.",
}

# Функция для команды /start
def questions(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        "Чтобы получить ответ на вопрос, выберите один из вариантов ниже:",
        reply_markup=get_questions_keyboard(),
    )

def call_manager(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Please enter your username:")
    return USERNAME

# Function to handle the username input
def receive_username(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data['username'] = update.message.text

    update.message.reply_text("Please enter your phone number:")
    return PHONE_NUMBER

# Function to handle the phone number input
def receive_phone_number(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data['phone_number'] = update.message.text

    # Create a custom keyboard with "Yes" and "No" buttons to verify data
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='yes')],
        [InlineKeyboardButton("No", callback_data='no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        f"Username: {user_data['username']}\nPhone Number: {user_data['phone_number']}\n\n"
        "Is this data correct? Please select 'Yes' or 'No' to verify.",
        reply_markup=reply_markup,
    )
    return VERIFY_DATA

def verify_data(update, context):
    query = update.callback_query
    user_data = context.user_data

    if query.data == 'yes':
        # Data is correct, set the 'verified' flag to True
        user_data['verified'] = True
        query.answer("Data verified. You can now ask questions using ChatGPT.")

    elif query.data == 'no':
        # Data is incorrect, reset the conversation
        query.answer("Data not verified. Please start over.")
        return ConversationHandler.END

def handle_text_message(update, context):
    user_message = update.message.text

    if context.user_data.get('verified', True):
        # If the user's data is verified, check if the message is a question
        if user_message in questions_answers:
            answer = questions_answers[user_message]
            update.message.reply_text(answer)
        else:
            # If not a question, proceed with ChatGPT interactions
            chatgpt_response = bot(user_message)  # Use your ChatGPT function here
            update.message.reply_text(chatgpt_response)
    else:
        # If the user's data is not verified, you can handle other interactions here
        update.message.reply_text("Please verify your data first by typing /call and providing your username and phone number.")


