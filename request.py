import json
import requests
from datetime import datetime

def send_data_to_api(name, phone):
    try:
        # Send a POST request to the specified URL with the JSON data
        response = requests.post(f"https://pprojects.bitrix24.kz/rest/4018/01eskqq9lz0k0rww/crm.lead.add.json?fields[NAME]={name}&fields[PHONE][0][VALUE]={phone}&fields[PHONE][0][VALUE_TYPE]=WORK&fields[TITLE]=Procars запрос на звонок")
        if response.status_code == 200:
            return "Data sent successfully."
        else:
            return "Failed to send data. Status code: " + str(response.status_code)
    except Exception as e:
        return "An error occurred: " + str(e)

