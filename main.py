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
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Ваш ИМТ: {int(data['weight']) / (int(data['height']) * int(data['height']) * 0.0001)}")
        else:
            await message.answer("Только числа! Теперь начинай заново...")
        await state.finish()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Начните с команды /start")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
