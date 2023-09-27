import os 
from dotenv import load_dotenv 
import gspread 

load_dotenv()

GOID = os.getenv("GOID")

def fetch_data():
        
    gc = gspread.service_account(filename='google/creds2.json')

    sh = gc.open_by_key(GOID)
    worksheet = sh.get_worksheet(0)  # Replace with the correct worksheet index
    data = worksheet.get_all_values()
    
    return data