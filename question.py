import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import bot as bot 
import request as req
# Ваш токен бота
TOKEN = "5907195764:AAENObL59xrfDu8HYgNDWkQf9dX0l43S0xw"

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
    elif selected_question.startswith(("+7708", "+8708", "8708","+7705","+7747","+7701","8701","8747")) and len(selected_question) == 12 or len(selected_question) == 11:
        req.send_data_to_api(user.first_name, selected_question)

        update.message.reply_text(f"{user.first_name}, {selected_question} ваши данные правильно заполнен? Если да, то нажмите Да, если нет, то нажмите Нет")    
        # update.message.reply_text("Спасибо за ваш номер телефона! Мы свяжемся с вами в ближайшее время.")   
        if selected_question == "да" or selected_question == "Да":
            update.message.reply_text("Спасибо за ваш номер телефона! Мы свяжемся с вами в ближайшее время.")   
        elif selected_question == "нет" or selected_question == "Нет":
            update.message.reply_text("Пожалуйста, введите ваш номер телефона еще раз.")
    elif selected_question.startswith(("+7708","+8708", "8708","+7705","+7747","+7701","8701","8747")) and len(selected_question) < 11:
        update.message.reply_text("Вы набрали неправильный номер телефона. Пожалуйста, попробуйте еще раз.")   

    else:
        answer = bot.bot_answer(selected_question)
        update.message.reply_text(answer)


    
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
def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("questions", questions))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, bot))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
