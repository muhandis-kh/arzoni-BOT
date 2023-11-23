import logging
from aiogram import types
import asyncpg
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import bot, dp, db
from data.config import ADMINS
from keyboards.default.menu_admin import menu_admin
from keyboards.default.user import random_film_ru
from states.user import UserStates
from aiogram.dispatcher import FSMContext

@dp.message_handler(CommandStart(), user_id=ADMINS, state='*')
async def start_admin(message: types.Message, state=FSMContext):
    await message.answer(f"{message.from_user.first_name} Xush kelibsiz\n\nNima ish bajaramiz?", reply_markup=menu_admin)
    await state.finish()
    
@dp.message_handler(commands=['start'], state='*')
async def show_channel(message: types.Message):
    language_code = message.from_user.language_code
    try:
        if language_code == 'en':
            language_code = 'en'
        elif language_code == 'ru':
            language_code = 'ru'
        elif language_code == 'uz':
            language_code = 'uz'
        else:
            language_code = 'other'
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username,
                                 language_code=message.from_user.language_code)
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"{user[1]} (<a href='tg://user?id={message.from_user.id}'>{('@'+ message.from_user.username) if message.from_user.username else (message.from_user.first_name)}</a>) bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(ADMINS[0], text=msg)
    except asyncpg.exceptions.UniqueViolationError:
        pass
    result = f"Iltimos mahsulot nomini lotin alifbosida, imlo qoidalariga amal qilgan holda yuboring"
    await message.answer(result)
  
