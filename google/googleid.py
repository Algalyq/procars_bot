import os 
from dotenv import load_dotenv 
import gspread 

load_dotenv()

GOID = os.getenv("GOID")

def fetch_data():
    gc = gspread.service_account(filename='google/creds2.json')
    sh = gc.open_by_key(GOID)
    worksheet = sh.get_worksheet(0) 
    data = worksheet.get_all_values()
    
    return data

def fetch_data_question():
    gc = gspread.service_account(filename='google/creds2.json')
    sh = gc.open_by_key(GOID)
    worksheet = sh.get_worksheet(1)  
    questions_answers = {}
    for row in worksheet.get_all_records():
        question = row['Question'] 
        answer = row['Answer']  
        questions_answers[question] = answer
    return questions_answers
