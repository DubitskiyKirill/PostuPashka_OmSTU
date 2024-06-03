import time

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

import database
from app.database import requests as rq
from app import keyboards as kb

user = Router()


class Process(StatesGroup):
    name = State()
    question = State()
    question2 = State()


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = await rq.add_user(message.from_user.id)
    if not user:
        await message.answer('Добро пожаловать!\n\nВведите ваше имя')
        await state.set_state(Process.name)
    else:
        await message.answer('Добро пожаловать!\n\nВведите ваше имя')
        await state.set_state(Process.name)


@user.message(Process.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Process.question)
    await message.answer('Напишите свой уникальный код поступающего.',
                         reply_markup=ReplyKeyboardRemove())



@user.message(Process.question)
async def get_question(message: Message, state: FSMContext):
    user = await state.get_data()
    await rq.edit_user(message.from_user.id,
                       user['name'],
                       message.from_user.username)
    await rq.add_ticket(message.text, message.from_user.id)
    await message.answer('Спасибо, произвожу поиск...')
    while True:
        time.sleep(60)
        await database.handle_message(message)

    await state.clear()