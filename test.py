
from datetime import date
import telebot 
import gspread

bot_token = '5907195764:AAF2QWHDtKSV30dJqKJsXKIlbQAr_hMGK9I'
googlesheet_id = '1usfr5PU5tThXr6kDOP7UOCDGdnrsg8yNoLpZ05ap3Hc'
bot = telebot.TeleBot(bot_token)
gc = gspread.service_account(filename='creds2.json')

# приветствуем пользователя и говорим что умеем..
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я буду записивать ваши расходы в таблицу. Введите расход через дефис в виде [КАТЕГОРИЯ-ЦЕНА]:")
    



@bot.message_handler(commands=['get_data'])
def get_data_from_sheet(message):
   
    worksheet = gc.open_by_key(googlesheet_id).sheet1
    pr = worksheet.get_values('A1:A10')
    print(pr)


if __name__ == '__main__':
     bot.polling(none_stop=True)