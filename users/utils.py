import requests
import xml.etree.ElementTree as ET
from decouple import config

SMS_NIKITA_URL = "https://smspro.nikita.kg/api/message"
SMS_NIKITA_LOGIN = config("SMS_NIKITA_LOGIN")
SMS_NIKITA_PASSWORD = config("SMS_NIKITA_PASSWORD")
SMS_NIKITA_SENDER = config("SMS_NIKITA_SENDER")


def send_sms(phone_number, pin):
    text = f"Код подтверждения: {pin}\nЕсли вы не запрашивали код, просто проигнорируйте это сообщение."
    
    message_id = "MSG" + str(abs(hash(phone_number + pin)) % (10 ** 12))
    
    xml_data = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
    <message>
        <login>{SMS_NIKITA_LOGIN}</login>
        <pwd>{SMS_NIKITA_PASSWORD}</pwd>
        <id>{message_id}</id>
        <sender>{SMS_NIKITA_SENDER}</sender>
        <text>{text}</text>
        <phones>
            <phone>{phone_number}</phone>
        </phones>
    </message>"""

    headers = {
        "Content-Type": "application/xml"
    }

    response = requests.post(SMS_NIKITA_URL, headers=headers, data=xml_data)

    return response.text
