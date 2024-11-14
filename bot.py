from telebot import TeleBot
from decouple import config 
import requests

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
bot = TeleBot(TELEGRAM_TOKEN)

@bot.callback_query_handler(func=lambda call: call.data.startswith('asd'))
def approve(call):
    chat_id = call.message.chat.id
    receipt_id = call.data.split('_')[1]

    bot.send_message(chat_id, 'Аххххххххххахахах сигма\nвот айди твоего чека: ', receipt_id, 'иди поплачь над этой информацией пупсек👩‍❤️‍💋‍')

@bot.callback_query_handler(func=lambda call: call.data.startswith('asd'))
def reject(call):
    chat_id = call.message.chat.id

    bot.send_message(chat_id, '🙄')