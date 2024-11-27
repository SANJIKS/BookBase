import requests
from decouple import config
from functools import wraps
from django.http import JsonResponse


INFOBIP_URL = config('INFOBIP_URL')
INFOBIP_API_KEY = config("INFOBIP_API_KEY")

url = f"https://{INFOBIP_URL}/sms/2/text/advanced"

def send_sms(phone_number, pin):
    text = f"Код подтверждения: {pin}\nЕсли вы не запрашивали код, просто проигнорируйте это сообщение."
    
    payload = {
        "messages": [
            {   
                "from": "Адалды Танда",
                "destinations": [
                    {
                        "to": phone_number
                    }
                ],
                "text": text
            }
        ]
    }

    headers = {
        'Authorization': f'App {INFOBIP_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # response = requests.post(url, headers=headers, json=payload)
    # return response.text
    print("AHAHAHHA")