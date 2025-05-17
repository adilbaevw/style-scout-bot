import logging
import os
from asos_parser import fetch_asos_new_dresses
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("👗 Привет! Я StyleScout — бот для поиска платьев. Напиши /scan для старта.")

@dp.message_handler(commands=['scan'])
async def send_scan(message: types.Message):
    await message.answer("🔍 Проверяю новинки с Asos...")
    items = await fetch_asos_new_dresses(limit=10)

    if not items:
        await message.answer("Не удалось найти новинки.")
        return

    for name, price, link in items:
        text = f"👗 {name}\n💶 {price}\n🌐 {link}"
        await message.answer(text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
