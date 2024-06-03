import sqlite3, os
import asyncio
from aiogram import Bot, Dispatcher, types
#from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.handlers import user as us
from app.database import requests as rq
from dotenv import load_dotenv
#from run import async_main
# Установите токен вашего бота

# Подключение к базе данных SQLite
conn = sqlite3.connect('scores.db', isolation_level=None)
cursor = conn.cursor()

# Инициализация бота и диспетчера
load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
# Инициализация планировщика
scheduler = AsyncIOScheduler()

# Функция для обработки сообщений от пользователя
async def handle_message(message: types.Message):
    user_text = message.text
    tg_id = message.from_user.id
    await us.rq.add_ticket(user_text, tg_id)
    if len(user_text) == 9:
        results = {}
        # Получение списка таблиц в базе данных
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        # Проход по таблицам и поиск текста
        for table_name in tables:
            table = table_name[0]
            cursor.execute(f"SELECT id FROM {table} WHERE Сумма_баллов LIKE ?", ('%' + user_text + '%',))
            ids = cursor.fetchall()
            if ids:
                results[table] = [row[0] for row in ids]
        # Отправка результатов пользователю
        if results:
            response = "Найденные совпадения:\n"
            for table, ids in results.items():
                response += f" {table} \n Текущая позиция: {', '.join(map(str, ids))}\n"
            await message.answer(response)
        else:
            await message.answer("Совпадений не найдено.")
    else:
        await message.answer("Пожалуйста, введите 9-значный текст.")
