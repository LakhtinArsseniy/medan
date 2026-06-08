import asyncio
import os
import gspread

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from oauth2client.service_account import ServiceAccountCredentials

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

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

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "medan-bot-523cee1f70ac.json",
    scope
)

client = gspread.authorize(creds)

sheet = client.open("MEDAN").sheet1

# =========================
# FSM
# =========================

class Appointment(StatesGroup):

    fullname = State()
    birthday = State()
    phone = State()

# =========================
# MENU
# =========================

def main_keyboard():

    kb = ReplyKeyboardBuilder()

    kb.button(text="👨‍⚕️ Лікарі")
    kb.button(text="🩺 Послуги")

    kb.button(text="🧾 УЗД")
    kb.button(text="🔬 Аналізи")

    kb.button(text="📞 Контакти")
    kb.button(text="🏠 Головне меню")

    kb.adjust(2, 2, 2)

    return kb.as_markup(resize_keyboard=True)

# =========================
# MAIN MENU
# =========================

async def open_main_menu(message):

    await message.answer(
        "🏥 <b>Головне меню</b>\n\n"
        "👇 Оберіть потрібний розділ",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )

# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message):

    photo = FSInputFile("photos/logo.jpg")

    text = (
        "🏥 <b>MEDAN</b>\n\n"
        "Медичний центр з турботою про вас 💙\n\n"
        "🔹 Онлайн запис\n"
        "🔹 УЗД та аналізи\n"
        "🔹 Консультації лікарів\n\n"
        "👇 Оберіть потрібний розділ"
    )

    await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )

# =========================
# FSM FULLNAME
# =========================

@dp.message(Appointment.fullname)
async def get_fullname(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        fullname=message.text
    )

    await message.answer(
        "🎂 Введіть дату народження:"
    )

    await state.set_state(
        Appointment.birthday
    )

# =========================
# FSM BIRTHDAY
# =========================

@dp.message(Appointment.birthday)
async def get_birthday(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        birthday=message.text
    )

    await message.answer(
        "📞 Введіть номер телефону:"
    )

    await state.set_state(
        Appointment.phone
    )

# =========================
# FSM PHONE
# =========================

@dp.message(Appointment.phone)
async def get_phone(
    message: Message,
    state: FSMContext
):


    await state.update_data(
        phone=message.text
    )

    data = await state.get_data()

    sheet.append_row([
        data["doctor"],
        data["day"],
        data["fullname"],
        data["birthday"],
        data["phone"]
    ])

    await message.answer(
        "✅ <b>Запис успішний!</b>\n\n"

        f"👨‍⚕️ Лікар: {data['doctor']}\n"
        f"📅 День: {data['day']}\n"
        f"⏰ Час: {data['time']}\n\n"

        f"👤 ПІБ: {data['fullname']}\n"
        f"🎂 Дата народження: {data['birthday']}\n"
        f"📞 Телефон: {data['phone']}\n\n"

        "📞 Адміністратор скоро зв'яжеться з вами.",

        parse_mode="HTML"
    )

    await state.clear()

# =========================
# BUTTONS
# =========================

@dp.message()
async def buttons(
    message: Message,
    state: FSMContext
):

    current_state = await state.get_state()

    if await state.get_state():
        return


    # MAIN MENU
    if message.text == "🏠 Головне меню":

        await open_main_menu(message)

    # DOCTORS
    elif message.text == "👨‍⚕️ Лікарі":

        doctors_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="❤️ Кардіолог",
                        callback_data="doctor_cardio"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="👩‍⚕️ Гінеколог",
                        callback_data="doctor_ginekolog"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🩺 Уролог",
                        callback_data="doctor_urolog"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🦴 Травматолог",
                        callback_data="doctor_travma"
                    )
                ]
            ]
        )

        await message.answer(
            "👨‍⚕️ <b>Оберіть лікаря:</b>",
            reply_markup=doctors_keyboard,
            parse_mode="HTML"
        )

    # SERVICES
    elif message.text == "🩺 Послуги":

        await message.answer(
            "🩺 <b>Послуги</b>\n\n"
            "• Внутрішньосуглобові ін'єкції\n"
            "• Блокади\n"
            "• Денний стаціонар\n"
            "• Видалення родимок\n"
            "• Радіохвильове видалення",
            parse_mode="HTML"
        )

    # UZD
    elif message.text == "🧾 УЗД":

        uzd_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="👩‍⚕️ Гінекологія",
                        callback_data="uzd_ginekologiya"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🩺 Урологія",
                        callback_data="uzd_urologiya"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❤️ Кардіологія",
                        callback_data="uzd_kardiologiya"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🩸 Судини",
                        callback_data="uzd_sudyny"
                    )
                ]
            ]
        )

        await message.answer(
            "🧾 <b>УЗД</b>\n\n👇 Оберіть напрямок:",
            reply_markup=uzd_keyboard,
            parse_mode="HTML"
        )

    # ANALYSES
    elif message.text == "🔬 Аналізи":

        await message.answer(
            "🔬 <b>Лабораторія</b>\n\n"
            "🕗 Пн–Пт: 08:00–11:30\n"
            "🕗 Субота: 08:00–11:00",
            parse_mode="HTML"
        )

    # CONTACTS
    elif message.text == "📞 Контакти":

        await message.answer(
            "📞 <b>Контакти</b>\n\n"
            "☎️ +380 XX XXX XX XX\n"
            "📍 м. Чугуїв",
            parse_mode="HTML"
        )

# =========================
# CALLBACKS
# =========================

@dp.callback_query()
async def callbacks(
    callback: CallbackQuery,
    state: FSMContext
):
    
    
    

    # =====================
    # DOCTOR
    # =====================
    if callback.data.startswith("doctor_"):

        doctor_name = callback.data.replace(
            "doctor_",
            ""
        )

        names = {
            "cardio": "❤️ Кардіолог",
            "ginekolog": "👩‍⚕️ Гінеколог",
            "urolog": "🩺 Уролог",
            "travma": "🦴 Травматолог"
        }

        doctor_title = names[doctor_name]

        await state.update_data(
            doctor=doctor_title
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📝 Записатися",
                        callback_data="open_days"
                    )
                ]
            ]
        )

        await callback.message.answer(
            f"{doctor_title}\n\n"
            "📞 +380 XX XXX XX XX\n"
            "👨‍⚕️ Прийом за записом",
            reply_markup=keyboard
        )

    # =====================
    # MAIN MENU
    # =====================

    elif callback.data == "main_menu":

        await open_main_menu(callback.message)

    # =====================
    # DAYS
    # =====================

    elif callback.data == "open_days":

        days_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="🟢 Пн 27.05",
                        callback_data="day_27.05"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🟢 Ср 29.05",
                        callback_data="day_29.05"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🔴 Пт 31.05",
                        callback_data="busy_day"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="main_menu"
                    )
                ]
            ]
        )

        await callback.message.answer(
            "📅 <b>Оберіть день:</b>",
            reply_markup=days_keyboard,
            parse_mode="HTML"
        )

    # =====================
    # BUSY DAY
    # =====================

    elif callback.data == "busy_day":

        await callback.answer(
            "❌ У цей день прийому немає",
            show_alert=True
        )

    # =====================
    # TIME
    # =====================

    elif callback.data.startswith("day_"):

        selected_day = callback.data.replace(
            "day_",
            ""
        )

        await state.update_data(
            day=selected_day
        )

        time_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="🟢 10:00",
                        callback_data="time_10:00"
                    ),

                    InlineKeyboardButton(
                        text="🔴 10:30",
                        callback_data="busy_time"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🟢 11:00",
                        callback_data="time_11:00"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="open_days"
                    )
                ]
            ]
        )

        await callback.message.answer(
            f"📅 День: {selected_day}\n\n"
            "⏰ <b>Оберіть час:</b>",

            reply_markup=time_keyboard,
            parse_mode="HTML"
        )

    # =====================
    # BUSY TIME
    # =====================

    elif callback.data == "busy_time":

        await callback.answer(
            "❌ Цей час зайнятий",
            show_alert=True
        )

    # =====================
    # SELECTED TIME
    # =====================

    elif callback.data.startswith("time_"):

        selected_time = callback.data.replace(
            "time_",
            ""
        )

        await state.update_data(
            time=selected_time
        )

        await callback.message.answer(
            "👤 Введіть ПІБ:"
        )

        await state.set_state(
            Appointment.fullname
        )

    elif callback.data == "uzd_ginekologiya":

        await callback.message.answer(
            "👩‍⚕️ УЗД Гінекологія"
        )

    elif callback.data == "uzd_urologiya":

        await callback.message.answer(
            "🩺 УЗД Урологія"
        )

    elif callback.data == "uzd_kardiologiya":

        await callback.message.answer(
            "❤️ УЗД Кардіологія"
        )

    elif callback.data == "uzd_sudyny":

        await callback.message.answer(
            "🩸 УЗД Судини"
        )

    await callback.answer()

# =========================
# START BOT
# =========================

async def main():

    print("Бот запущений!")

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())