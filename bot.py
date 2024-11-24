import logging, sys, asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from decouple import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.callback_query(F.data.startswith('confirm'))
async def approve_receipt(call: CallbackQuery):
    receipt_id = call.split('_')[1]
    await call.message.answer(
        f"Аххххххххххахахах сигма\n"
        f"Вот айди твоего чека: {receipt_id}\n"
        f"Иди поплачь над этой информацией, пупсек 👩‍❤️‍💋‍"
    )


@dp.callback_query(F.data.startswith('reject'))
async def reject_receipt(call: CallbackQuery):
    await call.message.answer("🙄")


@dp.message(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer('Salam Aleykum')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')