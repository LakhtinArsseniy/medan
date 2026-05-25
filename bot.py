import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv

# =========================
# TOKEN
# =========================

load_dotenv()

TOKEN = os.getenv("TOKEN")

# =========================
# BOT
# =========================

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =========================
# ГОЛОВНЕ МЕНЮ
# =========================

def main_keyboard():

    kb = ReplyKeyboardBuilder()

    kb.button(text="👨‍⚕️ Лікарі")
    kb.button(text="🩺 Послуги")

    kb.button(text="🧾 УЗД")
    kb.button(text="🔬 Аналізи")

    kb.button(text="📅 Графік")
    kb.button(text="📞 Контакти")

    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)

# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message):

    photo = FSInputFile("photos/logo.jpg")

    text = (
        "🏥 <b>MEDAN</b>\n\n"
        "Медичний центр з турботою про вас 💙\n\n"

        "🔹 Консультації лікарів\n"
        "🔹 УЗД та аналізи\n"
        "🔹 Денний стаціонар\n"
        "🔹 Сучасне обладнання\n\n"

        "👇 Оберіть потрібний розділ"
    )

    await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )

# =========================
# ОБРОБКА КНОПОК
# =========================

@dp.message()
async def buttons(message: Message):

    # ЛІКАРІ
    if message.text == "👨‍⚕️ Лікарі":

        doctors_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="❤️ Кардіолог",
                        callback_data="cardio"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="👩‍⚕️ Гінеколог",
                        callback_data="ginekolog"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🩺 Уролог",
                        callback_data="urolog"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🦴 Травматолог",
                        callback_data="travma"
                    )
                ]
            ]
        )

        await message.answer(
            "👨‍⚕️ <b>Оберіть лікаря:</b>",
            reply_markup=doctors_keyboard,
            parse_mode="HTML"
        )

    # ПОСЛУГИ
    elif message.text == "🩺 Послуги":

        await message.answer(
            "🩺 <b>Послуги медцентру</b>\n\n"

            "• Внутрішньосуглобові ін'єкції\n"
            "• Блокади\n"
            "• Денний стаціонар\n"
            "• Видалення родимок\n"
            "• Видалення папілом\n"
            "• Радіохвильове видалення",

            parse_mode="HTML"
        )

    # УЗД
    elif message.text == "🧾 УЗД":

        await message.answer(
            "🧾 <b>УЗД</b>\n\n"

            "• Гінекологія\n"
            "• Урологія\n"
            "• Кардіологія\n"
            "• Внутрішні органи\n"
            "• Судини",

            parse_mode="HTML"
        )

    # АНАЛІЗИ
    elif message.text == "🔬 Аналізи":

        await message.answer(
            "🔬 <b>Лабораторія</b>\n\n"

            "🕗 Пн – Пт: 08:00 – 11:30\n"
            "🕗 Субота: 08:00 – 11:00\n"
            "❌ Неділя: вихідний\n\n"

            "💬 Ціни на аналізи скоро будуть доступні.",

            parse_mode="HTML"
        )

    # ГРАФІК
    elif message.text == "📅 Графік":

        await message.answer(
            "📅 <b>Графік роботи</b>\n\n"

            "Пн – Пт: 08:00 – 18:00\n"
            "Субота: 09:00 – 15:00\n"
            "Неділя: вихідний",

            parse_mode="HTML"
        )

    # КОНТАКТИ
    elif message.text == "📞 Контакти":

        await message.answer(
            "📞 <b>Контакти</b>\n\n"

            "☎️ +380 XX XXX XX XX\n"
            "📍 м. Чугуїв\n"
            "🌐 Сайт: скоро буде",

            parse_mode="HTML"
        )

    # НЕВІДОМІ КНОПКИ
    else:

        await message.answer(
            "❗ Оберіть кнопку з меню нижче."
        )

# =========================
# CALLBACK КНОПКИ
# =========================

@dp.callback_query()
async def callbacks(callback: CallbackQuery):

    # КАРДІОЛОГ
    if callback.data == "cardio":

        await callback.message.answer(
            "❤️ <b>Кардіолог</b>\n\n"
            "📞 +380 XX XXX XX XX\n"
            "👨‍⚕️ Прийом за записом",
            parse_mode="HTML"
        )

    # ГІНЕКОЛОГ
    elif callback.data == "ginekolog":

        await callback.message.answer(
            "👩‍⚕️ <b>Гінеколог</b>\n\n"
            "📞 +380 XX XXX XX XX",
            parse_mode="HTML"
        )

    # УРОЛОГ
    elif callback.data == "urolog":

        await callback.message.answer(
            "🩺 <b>Уролог</b>\n\n"
            "📞 +380 XX XXX XX XX",
            parse_mode="HTML"
        )

    # ТРАВМАТОЛОГ
    elif callback.data == "travma":

        await callback.message.answer(
            "🦴 <b>Травматолог</b>\n\n"
            "📞 +380 XX XXX XX XX",
            parse_mode="HTML"
        )

    await callback.answer()

# =========================
# ЗАПУСК
# =========================

async def main():

    print("Бот запущений!")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())