import logging, sys, asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from decouple import config

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
BACKEND_URL = config("BACKEND_URL")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.callback_query(F.data.startswith('confirm_'))
async def approve_receipt(call: CallbackQuery):
    receipt_id = call.data.split('_')[1]
    response = requests.post(BACKEND_URL + f'/books/receipts/confirm/{receipt_id}/')
    if response.status_code == 404:
        await call.message.answer('Ошибка. \nЧек не найден.')
    elif response.status_code == 200:
        await call.message.answer(
            f"Чек подтвержден!"
        )
        await call.message.bot.delete_message(call.message.message_id)
    else:
        await call.message.answer('Произошла внутренняя ошибка')


@dp.callback_query(F.data.startswith('reject_'))
async def reject_receipt(call: CallbackQuery):
    await call.message.answer("Чек отклонен")
    await call.message.bot.delete_message(call.message.message_id)


@dp.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer('Салам Алейкум!\nЭтот бот будет оповещать о чеках пользователей приложении "Адалды Танда".')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')