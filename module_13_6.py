from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
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

API_TOKEN = "-----------------"
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рассчитать"), KeyboardButton(text="Информация")],
        [KeyboardButton(text="/start")]
    ],
    resize_keyboard=True
)

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")],
    [InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")]
])

@dp.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer(
        "Привет! Я помогу рассчитать вашу норму калорий.\n"
        "Нажмите 'Рассчитать', чтобы начать, или 'Информация', чтобы узнать больше.",
        reply_markup=keyboard
    )

@dp.message(F.text == "Информация")
async def info_command(message: Message):
    await message.answer(
        "Этот бот помогает рассчитать вашу дневную норму калорий на основе возраста, роста и веса.\n"
        "Нажмите 'Рассчитать', чтобы начать!"
    )

@dp.message(F.text == "Рассчитать")
async def main_menu(message: Message):
    await message.answer(
        "Выберите опцию:",
        reply_markup=inline_keyboard
    )

@dp.callback_query(F.data == "formulas")
async def get_formulas(call: CallbackQuery):
    await call.message.answer(
        "Формула Миффлина-Сан Жеора для мужчин:\n"
        "10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (лет) + 5\n\n"
        "Для женщин:\n"
        "10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (лет) − 161"
    )
    await call.answer()


@dp.callback_query(F.data == "calories")
async def set_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)
    await call.answer()


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


    calories = 10 * weight + 6.25 * growth - 5 * age + 5


    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в день.")


    await state.clear()


async def main():

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
