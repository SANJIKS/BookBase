import telebot
from telebot import TeleBot
from decouple import config

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
MODERATOR_CHAT_IDS = config('MODERATOR_CHAT_IDS').split(',')

bot  = TeleBot(TELEGRAM_TOKEN)

def send_receipt_to_moderator(receipt):
    receipt_photo_url = receipt.image.path
    with open(receipt_photo_url, 'rb') as photo:
        message = (
            f"Новый чек от {receipt.user.phone_number}.\n"
            f"Книга: {receipt.book.title}\n"
            f"Дата покупки: {receipt.uploaded_at}\n"
            f"Проверьте чек."
        )

        markup = telebot.types.InlineKeyboardMarkup()
        confirm_button = telebot.types.InlineKeyboardButton("Подтвердить", callback_data=f"confirm_{receipt.id}")
        reject_button = telebot.types.InlineKeyboardButton("Отклонить", callback_data=f"reject_{receipt.id}")
        markup.add(confirm_button, reject_button)

        for chat_id in MODERATOR_CHAT_IDS:
            bot.send_photo(chat_id, photo, caption=message, reply_markup=markup)