import logging, sys, asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from decouple import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


class ReceiptCallback(CallbackData, prefix="receipt"):
    action: str
    receipt_id: str


@dp.callback_query(ReceiptCallback.filter(action="confirm"))
async def approve_receipt(call: CallbackQuery, callback_data: ReceiptCallback):
    receipt_id = callback_data.receipt_id
    logger.info(f"User {call.from_user.id} confirmed receipt {receipt_id}")
    
    await call.message.answer(
        f"Аххххххххххахахах сигма\n"
        f"Вот айди твоего чека: {receipt_id}\n"
        f"Иди поплачь над этой информацией, пупсек 👩‍❤️‍💋‍"
    )


@dp.callback_query(ReceiptCallback.filter(action="reject"))
async def reject_receipt(call: CallbackQuery, callback_data: ReceiptCallback):
    logger.info(f"User {call.from_user.id} rejected receipt {callback_data.receipt_id}")
    
    await call.message.answer("🙄")


@dp.message(commands=["start"])
async def start_handler(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot.")
    
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="Confirm Receipt", callback_data=ReceiptCallback(action="confirm", receipt_id="12345")
    )
    keyboard.button(
        text="Reject Receipt", callback_data=ReceiptCallback(action="reject", receipt_id="12345")
    )
    keyboard.adjust(2)
    await message.answer("Choose an action:", reply_markup=keyboard.as_markup())



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')