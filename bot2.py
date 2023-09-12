import os
from dotenv import load_dotenv
import openai
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI,VectorDBQA 

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


def gpt(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_message = update.message.text
    out = model.run(user_message)
    print(out)
    update.message.reply_text(out)
# Register the ChatGPT handl
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, gpt))

if __name__ == "__main__":
    updater.start_polling()
    updater.idle()








# import os
# from dotenv import load_dotenv
# from langchain.vectorstores import Chroma
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain
# load_dotenv()

# os.environ['OPENAI_API_KEY'] = os.getenv("ai_token")


# persist_directory = 'Store/'
# embedding = OpenAIEmbeddings()
# vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# llm = ChatOpenAI(model_name="gpt-3.5-turbo-0301", temperature=0)


# template = """Используйте следующие фрагменты контекста, чтобы ответить на вопрос в конце. Если вы не знаете ответа, просто скажите, что вы не знаете, не пытайтесь придумать ответ. Используйте максимум три предложения. Старайтесь, чтобы ответ был как можно более кратким. Всегда говорите "спасибо, что спросили!" в конце ответа
# {context}
# Question: {question}
# Helpful Answer:"""
# QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)
# # Run chain
# from langchain.chains import RetrievalQA

# os.environ['OPENAI_API_KEY'] = os.getenv("ai_token")
# # # Define your Telegram bot token
# TOKEN = os.getenv("tg_token")

# # # # Create an Updater object
# updater = Updater(token=TOKEN, use_context=True)
# dispatcher = updater.dispatcher




# def gpt(update: Update, context: CallbackContext):
    
#     user_id = update.message.from_user.id
#     user_message = update.message.text
#     qa_chain = RetrievalQA.from_chain_type(llm,
#                                         retriever=vectordb.as_retriever(),
#                                         return_source_documents=True,
#                                         chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})


#     # result = qa_chain({"query": user_message})
#     memory = ConversationBufferMemory(
#         memory_key="chat_history",
#         return_messages=True

#     )


#     retriever=vectordb.as_retriever()
#     qa = ConversationalRetrievalChain.from_llm(
#         llm,
#         retriever=retriever,
#         memory=memory
#     )
#     result = qa({"question": user_message})
#     update.message.reply_text(result['answer'])

# dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, gpt))

# if __name__ == "__main__":
#     updater.start_polling()
#     updater.idle()

