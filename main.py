import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import dotenv_values

API_TOKEN = dotenv_values(".env").get('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


def messageIMT(imt):
    if imt < 16:
        return 'Выраженный дефицит массы тела'
    elif 16 <= imt < 18.5:
        return 'Недостаточная масса тела'
    elif 18.5 <= imt < 25:
        return 'Нормальная масса тела'
    elif 25 <= imt < 30:
        return 'Избыточная масса тела (предожирение)'
    elif 30 <= imt < 35:
        return 'Ожирение 1-ой степени'
    elif 35 <= imt <= 40:
        return 'Ожирение 2-ой степени'
    else:
        return 'Ожирение 3-ой степени'


class States(StatesGroup):
    height = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Введите рост!")
    await States.height.set()


@dp.message_handler(state=States.height)
async def load_height(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit():
            data['height'] = message.text
            await message.answer("Теперь введите вес!")
            await States.weight.set()
        else:
            await message.answer("Только числа! Теперь начинай заново...")
            await state.finish()


@dp.message_handler(state=States.weight)
async def load_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit():
            data['weight'] = message.text
            height = float(data['height'])
            weight = float(data['weight'])
            imt = weight / (height * height * 0.0001)
            await bot.send_message(chat_id=message.from_user.id, text=f"Ваш ИМТ: {imt}")
            await bot.send_message(chat_id=message.from_user.id, text=messageIMT(imt))

        else:
            await message.answer("Только числа! Теперь начинай заново...")
        await state.finish()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Начните с команды /start")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
