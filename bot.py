import asyncio
import os
import re

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
    kb.button(text="🗺️ Google Maps")
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

    photo = FSInputFile("photos/clinic.jpg")

    text = (
        "🏥 <b>MEDAN</b>\n\n"
        "Вас вітає Медичний Центр Medan!💙"
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

    phone = message.text.strip()

    pattern = r"^0\d{9}$"

    if not re.fullmatch(pattern, phone):
        await message.answer(
            "❌ Невірний номер телефону!\n\n"
            "Приклад: 0XXXXXXXXX"
        )
        return

    await state.update_data(
        phone=phone
    )

    data = await state.get_data()

    await message.answer(
        "✅ <b>Запис успішний!</b>\n\n"

        f"🧾 Послуга: {data.get('service', data['doctor'])}\n"
        f"💰 Вартість: {data.get('price', '-')}\n"
        f"⏱ Тривалість: {data.get('duration', '-')}\n\n"

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
            "• Радіохвильове видалення родимок, новусів, папілом",
            parse_mode="HTML"
        )

    # UZD
    elif message.text == "🧾 УЗД":

        uzd_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="🩺 Урологія",
                        callback_data="uzd_urology"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🩸 Судини",
                        callback_data="uzd_vessels"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🫀 Внутрішні органи",
                        callback_data="uzd_organs"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="👩 Гінекологія",
                        callback_data="uzd_gyn"
                    )
                ]
            ]
        )

        await message.answer(
            "🧾 <b>Оберіть напрямок УЗД</b>",
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

    # Google Maps
    elif message.text == "🗺️ Google Maps":

        maps_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📍 Відкрити карту",
                        url="https://maps.app.goo.gl/ВАШЕ_ПОСИЛАННЯ"
                    )
                ]
            ]
        )

        await message.answer(
            "📍 Натисніть кнопку нижче, щоб відкрити місцезнаходження медичного центру MEDAN.",
            reply_markup=maps_keyboard
        )

# CONTACTS
    elif message.text == "📞 Контакти":

        await message.answer(
            "📞 <b>Контакти</b>\n\n"
            "📍 м. Чугуїв\n"
            "🏠 вул. Леонова, 6Г\n\n"
            "☎️ +38 (098) 850-12-32",
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

    elif callback.data == "uzd_urology":

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="🟢 УЗД нирок",
                        callback_data="service_kidney"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🟢 УЗД сечового міхура",
                        callback_data="service_bladder"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🟢 УЗД простати",
                        callback_data="service_prostate"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🟢 УЗД мошонки",
                        callback_data="service_scrotum"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🟢 Нирки + сечовий міхур",
                        callback_data="service_kidney_bladder"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🟢 Сечовий міхур + простата",
                        callback_data="service_bladder_prostate"
                    )
                ]
            ]
        )

        await callback.message.answer(
            "🩺 <b>Оберіть послугу</b>",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    elif callback.data == "uzd_vessels":

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="🩸 Судини шиї",
                        callback_data="service_neck"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🦵 Артерії нижніх кінцівок",
                        callback_data="service_artery"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🦵 Вени нижніх кінцівок",
                        callback_data="service_vein"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🦵 Одна кінцівка (вени/артерії)",
                        callback_data="service_one_leg"
                    )
                ]
            ]
        )

        await callback.message.answer(
            "🩸 <b>Оберіть послугу</b>",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    elif callback.data == "uzd_organs":

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="🫀 Черевна порожнина",
                        callback_data="service_abdomen"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🩺 Нирки",
                        callback_data="service_kidneys2"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="❤️ Серце",
                        callback_data="service_heart"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="🦋 Щитовидна залоза",
                        callback_data="service_thyroid"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="💧 Сечовидільна система",
                        callback_data="service_urinary"
                    )
                ]
            ]
        )

        await callback.message.answer(
            "🫀 <b>Оберіть послугу</b>",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
    elif callback.data == "service_abdomen":

        await state.update_data(
            doctor="🫀 Внутрішні органи",
            service="УЗД черевної порожнини",
            price="650 грн",
            duration="20 хв"
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
            "🫀 УЗД черевної порожнини\n\n"
            "💰 650 грн\n"
            "⏱ 20 хв\n\n"
            "📌 Підготовка:\n"
            "5–6 годин не їсти.\n"
            "Воду можна пити у невеликій кількості.",
            reply_markup=keyboard
        )

    elif callback.data == "service_kidneys2":

        await state.update_data(
            doctor="🫀 Внутрішні органи",
            service="УЗД нирок",
            price="550 грн",
            duration="20 хв"
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
            "🩺 УЗД нирок\n\n"
            "💰 550 грн\n"
            "⏱ 20 хв",
            reply_markup=keyboard
        )

    elif callback.data == "service_heart":

        await state.update_data(
            doctor="🫀 Внутрішні органи",
            service="УЗД серця",
            price="650 грн",
            duration="20 хв"
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
            "❤️ УЗД серця\n\n"
            "💰 650 грн\n"
            "⏱ 20 хв",
            reply_markup=keyboard
        )

    elif callback.data == "service_thyroid":

        await state.update_data(
            doctor="🫀 Внутрішні органи",
            service="УЗД щитовидної залози",
            price="550 грн",
            duration="20 хв"
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
            "🦋 УЗД щитовидної залози\n\n"
            "💰 550 грн\n"
            "⏱ 20 хв",
            reply_markup=keyboard
        )

    elif callback.data == "service_urinary":

        await state.update_data(
            doctor="🫀 Внутрішні органи",
            service="УЗД органів сечовидільної системи",
            price="650 грн",
            duration="20 хв"
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
            "💧 УЗД органів сечовидільної системи\n\n"
            "💰 650 грн\n"
            "⏱ 20 хв",
            reply_markup=keyboard
        )


    elif callback.data == "service_kidney":

        await state.update_data(
            doctor="🩺 Урологія",
            service="УЗД нирок",
            price="550 грн",
            duration="20 хв"
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
            "🩺 УЗД нирок\n\n"
            "💰 550 грн\n"
            "⏱ 20 хв",
            reply_markup=keyboard
        )


    elif callback.data == "service_neck":

        await state.update_data(
            doctor="🩸 Судини",
            service="УЗД судин шиї",
            price="650 грн",
            duration="20 хв"
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
            "🩸 УЗД судин шиї\n\n"
            "💰 650 грн\n"
            "⏱ 20 хв",
            reply_markup=keyboard
        )

    elif callback.data == "uzd_gyn":

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="👩 УЗД органів малого тазу",
                        callback_data="service_pelvis"
                    )
                ]
            ]
        )

        await callback.message.answer(
            "👩 <b>Оберіть послугу</b>",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    elif callback.data == "service_pelvis":

        await state.update_data(
            doctor="👩 Гінекологія",
            service="УЗД органів малого тазу",
            price="600 грн",
            duration="20 хв"
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
            "👩 УЗД органів малого тазу\n\n"
            "💰 600 грн\n"
            "⏱ 20 хв",
            reply_markup=keyboard
        )


    elif callback.data == "service_artery":

        await state.update_data(
            doctor="🩸 Судини",
            service="УЗД артерій нижніх кінцівок",
            price="700 грн",
            duration="20 хв"
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
            "🩸 УЗД артерій нижніх кінцівок\n\n"
            "💰 700 грн\n"
            "⏱ 20 хв",
            reply_markup=keyboard
        )

    elif callback.data == "service_vein":

        await state.update_data(
            doctor="🩸 Судини",
            service="УЗД вен нижніх кінцівок",
            price="700 грн",
            duration="20 хв"
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
            "🩸 УЗД вен нижніх кінцівок\n\n"
            "💰 700 грн\n"
            "⏱ 20 хв",
            reply_markup=keyboard
        )

    elif callback.data == "service_one_leg":

        await state.update_data(
            doctor="🩸 Судини",
            service="УЗД вен або артерій однієї кінцівки",
            price="500 грн",
            duration="20 хв"
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
            "🩸 УЗД вен або артерій однієї кінцівки\n\n"
            "💰 500 грн\n"
            "⏱ 20 хв",
            reply_markup=keyboard
        )
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