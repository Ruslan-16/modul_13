from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F
import asyncio
import logging

API_TOKEN = "________________"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer("Привет! Я бот помогающий твоему здоровью.")

@dp.message(F.text)
async def all_messages(message: Message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer("Введите команду /start, чтобы начать общение.")

async def main():
    print("Бот запущен. Ожидаем сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
