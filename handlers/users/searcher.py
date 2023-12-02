from aiogram import types 
from loader import bot, dp, db
from urllib.parse import quote
import requests
from data.config import TOKEN, TOKEN_VERCEL, ADMINS
from pprint import pprint
from contextlib import suppress
from aiogram.utils.exceptions import MessageNotModified
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
import time


async def update_message(message: types.Message, new_value: str):
    with suppress(MessageNotModified):
      await message.edit_text(text=new_value)  

async def timer(message, i):
    clocks = ['🕐','🕑','🕒','🕓','🕔','🕖','🕗','🕘','🕙','🕚','🕛']
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=(message.message_id + 1), text=f"Bepul server cheklovlari sabab ma'lumotlar kutilmoqda. Iltimos biroz kuting {clocks[i]}") 

@dp.message_handler()
async def searcher(message: types.Message, state=FSMContext):

    text = message.text 
    encoded_query = quote(text)
    url_vercel = f"https://arzon-uz.vercel.app/search-product/?query={encoded_query}"
    url = f"https://arzon-uz.onrender.com/search-product/?query={encoded_query}"
    token = TOKEN
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    headers_vercel = {
        "Authorization": f"Bearer {TOKEN_VERCEL}",
        "Content-Type": "application/json",
    }
    
    
    try:
        response = requests.get(url_vercel, headers=headers_vercel)
    except Exception as e:
        print(e)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        await state.update_data({
            "data": data
        })


        keyboard = InlineKeyboardMarkup(row_width=1)

            
        if data['all']:

            for market, value in data['products'].items():
                if value:
                    pass
                else:
                    keyboard.insert(types.InlineKeyboardButton(text=f"Faqat {market.title()}dagi mahsulotlarni ko'rish", callback_data=f"market_{market}"))
            
            most_cheapest = data['all'][:5]
            anwer_text = f"<b>{text.upper()} UCHUN ENG ARZON NARXLAR</b>\n\n"
            for i, most_cheap in enumerate(most_cheapest,start=1):
                anwer_text += f"{i}. <b>Nomi:</b> {most_cheap['name']}\n<b>Narxi:</b> {'{:,}'.format(most_cheap['price'])} so'm\n<b>Link:</b> <a href='{most_cheap['link']}'>{most_cheap['name']}</a>\n<b>Marketplace:</b> {most_cheap['market_place']}\n\n____________________________________________________________________\n\n"
            
            await message.answer(text=anwer_text, reply_markup=keyboard)
        else:
            await message.answer(text=f"{text.upper()} UCHUN HECH QANDAY MA'LUMOT TOPILMADI")
    
    else:
        await message.answer("Bepul server cheklovlari sabab ma'lumotlar kutilmoqda. Iltimos biroz kuting 🕐")
        timeout_seconds = 30
        try:
            response = requests.get(url, headers=headers, timeout=timeout_seconds)       
        
        except requests.Timeout:
            await message.answer("Server bilan bog'liq muammolar borga o'xshaydi 🙇. Iltimos birozdan so'ng urunib ko'ring.")
             
        except Exception as e:
            print(e)
        
        if response.status_code == 200:
            data = response.json()
            await state.update_data({
                "data": data
            })
            
            keyboard = InlineKeyboardMarkup(row_width=1)
            
            if data['all']:
                
                for market, value in data['products'].items():
                    if value:
                        pass
                    else:
                        keyboard.insert(types.InlineKeyboardButton(text=f"Faqat {market.title()}dagi mahsulotlarni ko'rish", callback_data=f"market_{market}"))
                
                most_cheapest = data['all'][:5]
                anwer_text = f"<b>{text.upper()} UCHUN ENG ARZON NARXLAR</b>\n\n"
                for i, most_cheap in enumerate(most_cheapest,start=1):
                    anwer_text += f"{i}. <b>Nomi:</b> {most_cheap['name']}\n<b>Narxi:</b> {'{:,}'.format(most_cheap['price'])} so'm\n<b>Link:</b> <a href='{most_cheap['link']}'>{most_cheap['name']}</a>\n<b>Marketplace:</b> {most_cheap['market_place']}\n\n____________________________________________________________________\n\n"
                
                await message.answer(text=anwer_text, reply_markup=keyboard)
            else:
                await message.answer(text=f"{text.upper()} UCHUN HECH QANDAY MA'LUMOT TOPILMADI")
        else:
            print("error")
            
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('market_'))
async def process_book_button(callback_query: types.CallbackQuery, state=FSMContext):
    # Kelgan datadan market nomini olish
    market_name = callback_query.data.split('_')[1]
    # Mahsulot ma'lumotlarini olish uchun
    data = await state.get_data()
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    delete_mgs_btn = types.InlineKeyboardButton(text="❌", callback_data="delete_msg")
    keyboard.insert(delete_mgs_btn)
    data_market = data['data']['products'].get(market_name)
    anwer_text = f"<b>{market_name.upper()}DAGI ENG ARZON NARXLAR</b>\n\n"
    
    for i, product in enumerate(data_market,start=1):
            anwer_text += f"{i}. <b>Nomi:</b> {product['name']}\n<b>Narxi:</b> {'{:,}'.format(product['price'])} so'm\n<b>Link:</b> <a href='{product['link']}'>{product['name']}</a>\n\n____________________________________________________________________\n\n"
        
    await callback_query.message.answer(text=anwer_text, reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)
    
# Foydalanuvchiga yuborilgan mahsulot ma'lumotlarini foydalanuvchi o'chirib yuborish tugmasini bosganida ishlovchi funksiya
@dp.callback_query_handler(text_contains="delete_msg")
async def delete_msg(callback_query: types.CallbackQuery, state=FSMContext):
    message = callback_query.message
    
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        msg = f"Xabarni o'chirib yuborishda xatolik: {e}"
        await bot.send_message(chat_id=ADMINS[0], text=msg)