from aiogram import types 
from loader import bot, dp, db
from urllib.parse import quote
import requests
from data.config import TOKEN
from pprint import pprint
from contextlib import suppress
from aiogram.utils.exceptions import MessageNotModified

async def update_message(message: types.Message, new_value: str):
    with suppress(MessageNotModified):
      await message.edit_text(text=new_value)  

@dp.message_handler()
async def searcher(message: types.Message):

    text = message.text 
    encoded_query = quote(text)
    url = f"https://arzon-uz.onrender.com/search-product/?query={encoded_query}"
    token = TOKEN
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    await message.answer("Bepul server cheklovlari sabab ma'lumotlar kutilmoqda. Iltimos biroz kuting ⌛")
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print(e)

    # k = 0
    # messages = ["Bepul server cheklovlari sabab ma'lumotlar kutilmoqda. Iltimos biroz kuting ⌛", "Bepul server cheklovlari sabab ma'lumotlar kutilmoqda. Iltimos biroz kuting ⏳"]
    # while response.status_code == 200:
    #     await update_message(message=message, new_value=messages[k])
    #     if k == 0:
    #         k = 1
    #     else:
    #         k = 0
    if response.status_code == 200:
        data = response.json()
        most_cheapest = data['all'][:5]
        anwer_text = f"<b>{text.upper()} UCHUN ENG ARZON NARXLAR</b>\n\n"
        for most_cheap in most_cheapest:
            anwer_text += f"<b>Nomi:</b> {most_cheap['name']}\n<b>Narxi:</b> {'{:,}'.format(most_cheap['price'])} so'm\n<b>Link:</b> <a href='{most_cheap['link']}'>{most_cheap['name']}</a>\n<b>Marketplace:</b> {most_cheap['market_place']}\n\n____________________________________________________________________\n\n"
        
        await message.answer(text=anwer_text)
    else:
        print("error")