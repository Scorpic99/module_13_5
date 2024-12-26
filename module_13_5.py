from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import config


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Рассчитать'),
            KeyboardButton('Информация')
        ]
    ],resize_keyboard=True)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=main_menu)


@dp.message_handler(text="Информация")
async def btn_info(message: types.Message):
    await message.answer('Информация о боте')

@dp.message_handler(text="Рассчитать")
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()



@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()



@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calcul_calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваши калории составляют: {round(calcul_calories, 2)}')
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)