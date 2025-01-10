from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F
import asyncio
import logging

API_TOKEN = "______________"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    # Отправляем сообщение в чат
    await message.answer("Привет! Я бот, помогающий твоему здоровью. Напишите что-нибудь, и я отвечу вам!")

@dp.message(F.text)
async def all_messages(message: Message):
    # Ответ на любое текстовое сообщение
    await message.answer(f"Вы написали: {message.text}. Напишите или нажмите 👉/start, чтобы начать заново!")

async def main():
    print("Бот запущен. Ожидаем сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
