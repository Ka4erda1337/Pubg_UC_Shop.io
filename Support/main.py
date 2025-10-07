import asyncio
import json
import sqlite3
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

WEBAPP_URL = "https://ka4erda1337.github.io/Pubg_UC_Shop.io/"

bot = Bot(
    token="8281789014:AAFE4DAnRWxj-b0l5yzXMiPe3A5QtqRGpDQ",
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())

conn = sqlite3.connect('support.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS support_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        email TEXT,
        message TEXT,
        timestamp TEXT
    )
''')
conn.commit()

@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        user_id = message.from_user.id
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
            INSERT INTO support_messages (user_id, name, email, message, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, data['name'], data['email'], data['message'], timestamp))
        conn.commit()

        await message.answer("Сообщение поддержки сохранено!")
    except Exception as e:
        await message.answer(f"Ошибка при сохранении: {str(e)}")

@dp.message(F.text == "/support_list")
async def support_list(message: types.Message):
    ADMIN_ID = 123456789  # Замени на свой Telegram ID
    if message.from_user.id != ADMIN_ID:
        await message.answer("Доступ запрещён! Только для админа.")
        return

    cursor.execute('SELECT * FROM support_messages')
    rows = cursor.fetchall()

    if not rows:
        await message.answer("Нет сообщений в базе.")
        return

    response = "<b>Список сообщений поддержки:</b>\n\n"
    for row in rows:
        response += (
            f"ID: {row[0]}\n"
            f"User ID: {row[1]}\n"
            f"Имя: {row[2]}\n"
            f"Email: {row[3]}\n"
            f"Сообщение: {row[4]}\n"
            f"Время: {row[5]}\n\n"
        )

    await message.answer(response)

@dp.message(F.text.startswith("/delete_support"))
async def delete_support(message: types.Message):
    ADMIN_ID = 123456789  # Замени на свой Telegram ID
    if message.from_user.id != ADMIN_ID:
        await message.answer("Доступ запрещён! Только для админа.")
        return

    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer("Использование: /delete_support <id>")
            return

        msg_id = int(parts[1])
        cursor.execute('DELETE FROM support_messages WHERE id = ?', (msg_id,))
        conn.commit()

        if cursor.rowcount > 0:
            await message.answer(f"Сообщение ID {msg_id} удалено.")
        else:
            await message.answer("Сообщение не найдено.")
    except ValueError:
        await message.answer("ID должен быть числом.")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        "<b>🔥 Добро пожаловать в UC SHOP PUBG MOBILE!</b>\n\n"
        "💎 Здесь ты можешь приобрести UC по самым выгодным ценам!\n\n"
        "👉 Нажми кнопку ниже, чтобы открыть <i>приложение</i> и выбрать нужный пакет.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="💠 Открыть магазин UC",
                    web_app=WebAppInfo(url=WEBAPP_URL + "Support/index.html")
                )
            ]]
        )
    )

@dp.message(F.text == "/app")
async def app_handler(message: types.Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💠 Открыть магазин UC", web_app=WebAppInfo(url=WEBAPP_URL + "Support/index.html"))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Выбери кнопку ниже и переходи в WebApp 👇", reply_markup=markup)

async def main():
    print("✅ Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())