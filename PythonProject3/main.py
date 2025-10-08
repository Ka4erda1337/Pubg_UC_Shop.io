import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# URL твоего мини-приложения (замени на свой)
WEBAPP_URL = "https://ka4erda1337.github.io/Pubg_UC_Shop.io/"

# Инициализация бота
bot = Bot(
    token="8281789014:AAFE4DAnRWxj-b0l5yzXMiPe3A5QtqRGpDQ",
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())

# Команда /start
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
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]]
        )
    )

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
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]]
        )
    )@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        "<b>🔥 Добро пожаловать в UC SHOP PUBG MOBILE!</b>\n\n"
        "💎 Здесь ты можешь приобрести UC по самым выгодным ценам!\n\n"
        "👉 Нажми кнопку ниже, чтобы открыть <i>приложение</i> и выбрать нужный пакет.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="💠 Открыть магазин UC",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]]
        )
    )

# Команда /app
@dp.message(F.text == "/app")
async def app_handler(message: types.Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💠 Открыть магазин UC", web_app=WebAppInfo(url=WEBAPP_URL))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Выбери кнопку ниже и переходи в WebApp 👇", reply_markup=markup)

# Запуск бота
async def main():
    print("✅ Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
