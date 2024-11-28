import telebot
from telebot import TeleBot
from decouple import config

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
MODERATOR_CHAT_IDS = config('MODERATOR_CHAT_IDS').split(',')

bot  = TeleBot(TELEGRAM_TOKEN)

def send_receipt_to_moderator(receipt):
    for chat_id in MODERATOR_CHAT_IDS:
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

            bot.send_photo(chat_id, photo, caption=message, reply_markup=markup)

import PyPDF2
from pdf2image import convert_from_path
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Book, Page

from django.core.files.base import ContentFile

def add_pdf_as_book(pdf_file):
    # Чтение PDF файла
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    
    # Создание книги
    pdf_content = ContentFile(pdf_file.read())  # Читаем и оборачиваем PDF в ContentFile
    book = Book.objects.create(
        title=pdf_file.name,  # Можно взять имя файла как название
        # content=pdf_content   # Сохраняем сам файл PDF через ContentFile
    )
    
    # Преобразуем страницы в изображения и сохраняем их как отдельные страницы
    pages = convert_from_path(pdf_file, 300)  # 300 - разрешение
    for page_number, page in enumerate(pages, start=1):
        # Сохраняем страницу как изображение
        image_io = BytesIO()
        page.save(image_io, 'PNG')
        image_io.seek(0)
        
        # Сохраняем изображение на диск
        file_name = f'{book.title}_page_{page_number}.png'
        page_file = ContentFile(image_io.read(), name=file_name)
        
        # Создаем запись для страницы
        Page.objects.create(
            book=book,
            content=page_file,
            number=page_number
        )

    return book
