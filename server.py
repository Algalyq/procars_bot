from flask import Flask, request
import telebot

app = Flask(__name__)

# Initialize your Telegram bot using the bot token
bot = telebot.TeleBot(TOKEN)

# Define your route to handle incoming updates from Telegram
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update_json = request.get_json()
    update = telebot.types.Update.de_json(update_json)
    
    # Handle the update using your existing code
    dispatcher.process_new_updates([update])
    
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
