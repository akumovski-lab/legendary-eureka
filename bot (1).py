import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Токен берётся из переменной окружения BOT_TOKEN.
# Локально можно временно вписать напрямую вместо os.environ[...],
# но на Railway / GitHub токен в код лучше не вставлять.
TOKEN = os.environ.get("BOT_TOKEN", "ВАШ_ТОКЕН_СЮДА")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

START_TEXT = (
    "Привет! Я КиноПодбор 🎬\n"
    "Отвечай на вопрос — подберу что посмотреть."
)

MOOD_TEXT = "Какое настроение?"

RESULT_TEXT = (
    "Вот что можно посмотреть 🎬\n\n"
    "Фильмы: «1+1», «Начало», «Тихое место», «Зелёная миля», «Гранд Будапешт Отель»\n"
    "Сериалы: «Одни из нас», «Офис», «Настоящий детектив», «Тьма», «Друзья»"
)

ABOUT_TEXT = (
    "КиноПодбор помогает быстро найти что посмотреть — "
    "отвечаешь на вопрос, получаешь подборку."
)

HELP_TEXT = "Если что-то не работает — напиши нам, мы читаем все сообщения."


def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подобрать", callback_data="mood")],
        [InlineKeyboardButton(text="О боте", callback_data="about")],
    ])


def mood_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Посмеяться 😂", callback_data="result"),
            InlineKeyboardButton(text="Подумать 🎭", callback_data="result"),
        ],
        [
            InlineKeyboardButton(text="Пощекотать нервы 😱", callback_data="result"),
            InlineKeyboardButton(text="Полегче 🍿", callback_data="result"),
        ],
    ])


def result_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подобрать ещё раз", callback_data="mood")],
        [InlineKeyboardButton(text="Главное меню", callback_data="start")],
    ])


def about_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать подбор", callback_data="mood")],
        [InlineKeyboardButton(text="Главное меню", callback_data="start")],
    ])


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(START_TEXT, reply_markup=start_kb())


@dp.callback_query(F.data == "start")
async def cb_start(callback: CallbackQuery):
    await callback.message.edit_text(START_TEXT, reply_markup=start_kb())
    await callback.answer()


@dp.callback_query(F.data == "mood")
async def cb_mood(callback: CallbackQuery):
    await callback.message.edit_text(MOOD_TEXT, reply_markup=mood_kb())
    await callback.answer()


@dp.callback_query(F.data == "result")
async def cb_result(callback: CallbackQuery):
    await callback.message.edit_text(RESULT_TEXT, reply_markup=result_kb())
    await callback.answer()


@dp.callback_query(F.data == "about")
async def cb_about(callback: CallbackQuery):
    await callback.message.edit_text(ABOUT_TEXT, reply_markup=about_kb())
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
