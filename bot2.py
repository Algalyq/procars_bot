
import os
from dotenv import load_dotenv
import openai
from telegram import Update
from telegram.ext import Updater, MessageHandler,CommandHandler,CallbackContext, CallbackQueryHandler, Filters, CallbackContext
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI,VectorDBQA 
import callbacks as call
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader

import nltk
import getpass
# # Load environment variables from .env file
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("ai_token")
# # Define your Telegram bot token
TOKEN = os.getenv("tg_token")

# # # Create an Updater object
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Initialize OpenAI
openai.api_key = os.getenv("ai_token")

# Dictionary to store conversation history
conversation_history = {}

os.environ['OPENAI_API_KEY'] = os.getenv("ai_token")  

loader = DirectoryLoader("Store", glob='**/*.txt')
docs = loader.load()


char_text_split = CharacterTextSplitter(chunk_size=10000,chunk_overlap=0)
doc_texts = char_text_split.split_documents(docs)


openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

chat_params = {
        "model": "gpt-3.5-turbo-16k", # Bigger context window
        "openai_api_key": os.environ['OPENAI_API_KEY'],
        "temperature": 0.5, # To avoid pure copy-pasting from docs lookup
        "max_tokens": 8192
    }
vStore = Chroma.from_documents(doc_texts, openAI_embeddings)

model = VectorDBQA.from_chain_type(llm=ChatOpenAI(**chat_params),chain_type="stuff",vectorstore=vStore)
def bot_answer(text:str):
       
    # Define a system message to instruct the assistant
    system_message = "Вы - помощник компаний Profusion Cars. Ваша роль заключается в том, чтобы помочь пользователю найти автомобиль своей мечты. Пожалуйста, не отвечайте на вопросы по-английски"

    # Concatenate the user's message with the system message to simulate a conversation
    conversation = f"{system_message}\nUser: {text}"

    # Pass the conversation to the model and get a response
    out = model.run(conversation)

    # Extract the assistant's response from the conversation
    assistant_response = out.split("User: ")[-1]
    return assistant_response

def gpt(update: Update, context: CallbackContext):
    user_message = update.message.text

    # Define a system message to instruct the assistant
    system_message = "Вы - помощник компаний Profusion Cars. Ваша роль заключается в том, чтобы помочь пользователю найти автомобиль своей мечты. Пожалуйста, не отвечайте на вопросы по-английски"

    # Concatenate the user's message with the system message to simulate a conversation
    conversation = f"{system_message}\nUser: {user_message}"

    # Pass the conversation to the model and get a response
    out = model.run(conversation)

    # Extract the assistant's response from the conversation
    assistant_response = out.split("User: ")[-1]

    print(assistant_response)
    update.message.reply_text(assistant_response)
# Register the ChatGPT handl

dispatcher.add_handler(CommandHandler('car', call.cars))
dispatcher.add_handler(CallbackQueryHandler(call.show_company_models, pattern=r'show_company_'))
dispatcher.add_handler(CallbackQueryHandler(call.show_model_description, pattern=r'show_model_'))
dispatcher.add_handler(CallbackQueryHandler(call.show_complete_set_details, pattern=r'show_set_'))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, gpt))

if __name__ == "__main__":
    updater.start_polling()
    updater.idle()







