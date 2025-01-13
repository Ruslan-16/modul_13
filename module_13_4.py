from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

API_TOKEN = "_______________--"
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer("Бот работает! Напишите 'Calories'.")


@dp.message(F.text.lower() == "calories")
async def set_age(message: Message, state: FSMContext):
    await message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)


@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    age = message.text


    if not age.isdigit():
        await message.answer("Возраст должен быть числом. Попробуйте ещё раз:")
        return

    await state.update_data(age=int(age))
    await message.answer("Введите свой рост (в см):")
    await state.set_state(UserState.growth)


@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    growth = message.text

    if not growth.isdigit():
        await message.answer("Рост должен быть числом. Попробуйте ещё раз:")
        return

    await state.update_data(growth=int(growth))
    await message.answer("Введите свой вес (в кг):")
    await state.set_state(UserState.weight)

@dp.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    weight = message.text

    if not weight.isdigit():
        await message.answer("Вес должен быть числом. Попробуйте ещё раз:")
        return

    await state.update_data(weight=int(weight))

    data = await state.get_data()
    age = data.get("age")
    growth = data.get("growth")
    weight = data.get("weight")

    calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в день.")

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
