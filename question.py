import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import bot as bot 
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import request as req
from validator import validation

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

# Функция для создания клавиатуры с вопросами
def get_questions_keyboard():
    keyboard = []
    for question in questions_answers.keys():
        keyboard.append([question])
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

# Функция для обработки выбора вопроса
def answer_question(update: Update, context: CallbackContext) -> None:
    selected_question = update.message.text

    user = update.effective_user
    if selected_question in questions_answers:
        answer = questions_answers[selected_question]
        update.message.reply_text(answer)
        
    elif validation.validation_phone_number(selected_question) == True:
        # Store the phone number in user_data
        context.user_data['phone_number'] = selected_question

        # Create the custom keyboard with "Да" and "Нет" buttons
        keyboard = [
            [InlineKeyboardButton("Да", callback_data='yes')],
            [InlineKeyboardButton("Нет", callback_data='no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            text=f"{user.username }, {selected_question} ваши данные правильно заполнены? Если да, то нажмите Да, если нет, то нажмите Нет",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif validation.validation_phone_number(selected_question) == False:
        update.message.reply_text("Вы набрали неправильный номер телефона. Пожалуйста, попробуйте еще раз.")   

    else:
        answer = bot.bot_answer(selected_question)
        update.message.reply_text(answer)

def confirm(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = update.effective_user
    user_data = context.user_data

    if query.data == 'yes':
        # If user clicked "Да," make a POST request here using user_data['phone_number']
        phone_number = user_data.get('phone_number', '')
        if phone_number:
            req.send_data_to_api(user.first_name, phone_number)
            update.callback_query.answer("Данные успешно отправлены!")

    elif query.data == 'no':
        # Handle "Нет" case if needed
        pass
    
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    
    instructions = (
        f"Привет, {user.mention_html()} , !\n"
        "Я чат бот компаний Profusion Cars.Я помогу вам найти ответы на вопросы касаемо машины,комплектаций,цены и т.д.\n"
        "Вы можете задать вопрос в чат бот или через /questions посмотреть ответы на часто задаваемый вопросы \n\n"
        "Доступные команды:\n"
        "/questions - Показать это ответы на часто задаваемые вопросы\n"
        "/cars - Показать список машин и комплектаций,характеристики\n"
        "/call - Звонок от менеджера\n"
    )
    
    update.message.reply_html(instructions)
# Основная функция
