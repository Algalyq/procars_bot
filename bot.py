from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI,VectorDBQA 

from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader
# import magic


import os
import nltk


load_dotenv()


os.environ['OPENAI_API_KEY'] = os.getenv("ai_token")    

loader = DirectoryLoader("Store", glob='**/*.txt')
docs = loader.load()


char_text_split = CharacterTextSplitter(chunk_size=4000,chunk_overlap=0)
doc_texts = char_text_split.split_documents(docs)



openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

vStore = Chroma.from_documents(doc_texts, openAI_embeddings)

model = VectorDBQA.from_chain_type(llm=OpenAI(),chain_type="stuff",vectorstore=vStore)

questions = "Какой типа тип кузова у bmw x5" 

print(model.run(questions))
# import os
# from dotenv import load_dotenv
# import openai
# from telegram import Update
# from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
# from langchain.document_loaders import TextLoader
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import Chroma

# import os
# import getpass
# # # Load environment variables from .env file
# load_dotenv()


# os.environ['OPENAI_API_KEY'] = os.getenv("ai_token")
# # Define your Telegram bot token
# TOKEN = os.getenv("tg_token")

# # Create an Updater object
# updater = Updater(token=TOKEN, use_context=True)
# dispatcher = updater.dispatcher

# # Initialize OpenAI
# openai.api_key = os.getenv("ai_token")

# # Dictionary to store conversation history
# conversation_history = {}

# def gpt(update: Update, context: CallbackContext):
#     user_id = update.message.from_user.id
#     user_message = update.message.text

#     # Retrieve conversation history for this user
#     conversation = conversation_history.get(user_id, [])

#     # Append the user's message to the conversation
#     conversation.append({"role": "user", "content": user_message})

#     # Set up the chat input with conversation history
#     chat_input = [{"role": item["role"], "content": item["content"]} for item in conversation]

#     # Call the GPT model with conversation history
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=chat_input,
#     )

#     # Extract the GPT's reply from the response
#     gpt_reply = response.choices[0].message["content"]

#     # Append GPT's reply to the conversation
#     conversation.append({"role": "assistant", "content": gpt_reply})

#     # Store the updated conversation history
#     conversation_history[user_id] = conversation

#     # Send the GPT's reply to the user
#     raw_documents = TextLoader('./state_of_car.txt').load()
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     documents = text_splitter.split_documents(raw_documents)
#     query = user_message

#     db = Chroma.from_documents(documents, OpenAIEmbeddings())
   

#     embedding_vector = OpenAIEmbeddings().embed_query(query)
   
#     docs = db.similarity_search_by_vector(embedding_vector)
#     print(docs[0].page_content)
#     update.message.reply_text(docs[0].page_content)

# # Register the ChatGPT handler
# dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, gpt))

# if __name__ == "__main__":
#     updater.start_polling()
#     updater.idle()
