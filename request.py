import json
import requests
from datetime import datetime

def send_data_to_api(name, phone):
    # Create a Python dictionary with the provided strings and current timestamp
    data = {
        "name": name,
        "phone": phone,
        "timestamp": str(datetime.now())
    }

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data)

    try:
        # Send a POST request to the specified URL with the JSON data
        response = requests.post(post_url, data=json_data, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            return "Data sent successfully."
        else:
            return "Failed to send data. Status code: " + str(response.status_code)
    except Exception as e:
        return "An error occurred: " + str(e)

