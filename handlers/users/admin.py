from aiogram import types
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from states.admin import AdminState
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import asyncpg
from datetime import datetime
from datetime import date
from aiogram.utils.exceptions import BotBlocked
from keyboards.default.menu_admin import (backBtn, channels_keyboards, languagesButton,
    menu_admin, miniads_keyboards, verifyBtn, yesOrNo)
import re

link_regex = r"(https?:\/\/)?(www[.])?(telegram|t)\.me\/([a-zA-Z0-9_-]*)\/[0-9]\/?"

@dp.message_handler(text="Bekor qilish", user_id=ADMINS, state="*")
async def backButton(message: types.Message, state: FSMContext):
    await message.answer("Amal bekor qilindi", reply_markup=menu_admin)
    await state.finish()
@dp.message_handler(text="Obuna bo'lganlar soni", user_id=ADMINS)
async def check_subs(message: types.Message, state=FSMContext):
    channels_data = await db.select_channel_is_active()
    backBtn = KeyboardButton("Bekor qilish")
    global ChannelsKeys
    ChannelsKeys = ReplyKeyboardMarkup(resize_keyboard=True)
    k = 1
    if channels_data:
        for channel in channels_data:
            chat = await bot.get_chat(channel['username'])
            button = KeyboardButton(chat.title)
            ChannelsKeys.add(button)

        ChannelsKeys.add(backBtn)
  
        await message.answer("Kanallardan birini tanlang", reply_markup=ChannelsKeys)
        await AdminState.checkSub.set()
    else:
        await message.answer("Kanallar yo'q")
@dp.message_handler(state=AdminState.checkSub, user_id=ADMINS)
async def check_subs(message: types.Message, state=FSMContext):  
    text = message.text
    users = await db.select_all_users()
    channels_data = await db.select_channel_is_active()

    member = 0
    nomember = 0
    k = 0
    for channel in channels_data:   
        if text == channel['name']:
            for user in users:
                data = await bot.get_chat_member(chat_id=channel['username'], user_id=user[3])
                if data.status == 'member':
                    member += 1
                else:
                    nomember += 1
            await message.answer(f"<a href='https://t.me/{channel['username'].lstrip('@')}'><b>{channel['name']}</b></a>\nLimit: {channel['limit_user']}\nObuna bo'lganlar: {member}")
            
            try:
                if channel['limit_user'] <= member:
                    await db.deactive_channel(channel['username'])
                    await message.answer(f"{channel['username']} kanali deactive qilindi")
            except Exception as e:
                print(e)
        else:
            k += 1
    
    if k == len(channels_data):    
        await message.answer("Tugmalardan biri tanlanishi shart", reply_markup=ChannelsKeys)
            
        


@dp.message_handler(text="Majburiy obuna kanallari ustida amallar", user_id=ADMINS)
async def add_new(message: types.Message):
    await message.answer("Tugmalardan birini tanlang", reply_markup=channels_keyboards)
    await AdminState.channels.set()

@dp.message_handler(text="Active foydalanuvchilar soni", user_id=ADMINS)
async def add_new(message: types.Message):
    count_active_users = await db.select_all_details()
    await message.answer(count_active_users[0]['active_users'])   

@dp.message_handler(text="📊 Statistika", user_id=ADMINS)
async def statistic(message: types.Message, state=FSMContext):
    users = await db.select_all_users()
    active_users_count = 0
    deactive_users_count = 0
    if users:
        
        for user in users:
            user_id = user[3]
            try:
                await bot.send_chat_action(chat_id=user_id, action='typing')
                active_users_count += 1
            except BotBlocked:
                deactive_users_count += 1
            except Exception as e:
                print(e)
                pass
                
        active_users_count_db = await db.count_active_users()
        deactive_users_count_db = await db.count_deactive_users()
        
        if active_users_count > active_users_count_db:
            await db.update_active_users(active_users_count, 1)
        
        if deactive_users_count > deactive_users_count_db:
            await db.update_deactive_users(deactive_users_count, 1) 
        
        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        all_users_count = await db.count_users()
        en = await db.select_all_user_count_by_lang(language_code='en')  
        ru = await db.select_all_user_count_by_lang(language_code='ru')
        uz = await db.select_all_user_count_by_lang(language_code='uz')
        other = await db.select_all_user_count_by_lang(language_code='other')
        month = await db.count_users_by_month()
        day = await db.count_users_by_day()
        
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        current_date = date.today()
        
        for i in day:
            if i['d'] == current_date:
                day = i['count']
            else:
                day = 0
        
           
        currentDatetime = f"{currentYear}-{'0'+str(currentMonth) if len(str(currentMonth)) == 1 else currentMonth}-01"
        for i in month:
            if str(i['m']) in currentDatetime:
                month = i['count']
            else:
                month = 0
            
        msg = f"""📊 BOT STATISTIKASI: {dt_string} holatiga ko'ra
▪️Foydalanuvchilar: - {all_users_count}
▫️Faol: - {active_users_count}
▫️O'chirilgan: - {deactive_users_count}
▫️Bugun qo'shilgan a'zolar: - {day}
▫️Bu oy qo'shilgan a'zolar: - {month}
 English 🏴󠁧󠁢󠁥󠁮󠁧󠁿 - {en[0]['count']}
 O'zbekcha 🇺🇿 - {uz[0]['count']}
 Русский 🇷🇺 - {ru[0]['count']}
 Boshqalar - {other[0]['count']}
                """
        await message.answer(msg)
    else:
        await message.answer("Bazada ro'yhatdan o'tgan foydalanuvchilar yo'q", reply_markup=menu_admin)
        await state.finish()
        

@dp.message_handler(text="REKLAMA", user_id=ADMINS)
async def send_ads(message: types.Message):
    await message.answer("Reklama matnini yuboring", reply_markup=ReplyKeyboardRemove())

    await AdminState.ads_verify.set()

@dp.message_handler(state=AdminState.ads_verify, content_types=types.ContentType.PHOTO)    
async def verifyMessage(message: types.Message):    
    global file_id
    global caption
    global content_type

    file_id = message.photo[-1].file_id
    caption = message.caption if message.caption else False
    content_type = 'photo'

    await message.answer_photo(file_id, caption=caption if caption else None)
    await message.reply("Xabar foydalanuvchilarga shunday shaklda yetib boradi. Yuborishni davom ettirmoqchimisiz?", reply_markup=yesOrNo)
    await AdminState.yesOrNo.set()

@dp.message_handler(state=AdminState.ads_verify, content_types=types.ContentType.VIDEO)
async def verifyMessage(message: types.Message):
    global file_id
    global content_type
    global caption
    file_id = message.video.file_id
    caption = message.caption if message.caption else False
    content_type = 'video'

    await message.answer_video(file_id, caption=caption if caption else None)
    await message.reply("Xabar foydalanuvchilarga shunday shaklda yetib boradi. Yuborishni davom ettirmoqchimisiz?", reply_markup=yesOrNo)
    await AdminState.yesOrNo.set()

@dp.message_handler(state=AdminState.ads_verify, content_types=types.ContentType.STICKER)
async def verifyMessage(message: types.Message):
    global file_id
    global content_type
    file_id = message.sticker.file_id
    content_type = 'sticker'

    await message.answer_sticker(file_id)
    await message.reply("Xabar foydalanuvchilarga shunday shaklda yetib boradi. Yuborishni davom ettirmoqchimisiz?", reply_markup=yesOrNo)
    await AdminState.yesOrNo.set()

@dp.message_handler(state=AdminState.ads_verify, content_types=types.ContentType.TEXT)
async def verifyMessage(message: types.Message):
    global content_type
    global context
    content_type = 'text'
    context = message.text
    await message.answer(message.text)
    await message.reply("Xabar foydalanuvchilarga shunday shaklda yetib boradi. Yuborishni davom ettirmoqchimisiz?", reply_markup=yesOrNo)
    await AdminState.yesOrNo.set()

@dp.message_handler(state=AdminState.ads_verify, content_types=types.ContentType.DOCUMENT)
async def verifyMessage(message: types.Message):
    global content_type
    global file_id
    global caption
    file_id = message.document.file_id
    caption = message.caption if message.caption else False
    content_type = 'document'

    await message.answer_document(file_id, caption=caption if caption else None)
    await message.reply("Xabar foydalanuvchilarga shunday shaklda yetib boradi. Yuborishni davom ettirmoqchimisiz?", reply_markup=yesOrNo)
    await AdminState.yesOrNo.set()

@dp.message_handler(state=AdminState.ads_verify, content_types=types.ContentType.POLL)
async def verifyMessage(message: types.Message):
    global content_type
    global question
    global options2
    question = message.poll.question
    options = message.poll.options
    options2 = []
    for op in options:
        options2.append(op.text)
    content_type = 'poll'
    await message.answer_poll(question=question, options=options2)

    await message.reply("Xabar foydalanuvchilarga shunday shaklda yetib boradi. Yuborishni davom ettirmoqchimisiz?", reply_markup=yesOrNo)
    await AdminState.yesOrNo.set()

@dp.message_handler(state=AdminState.yesOrNo)
async def send_ad(message: types.Message, state=FSMContext):
    text = message.text

    if text == "⏭ Ha":
        await message.answer("Qaysi tildagi foydalanuvchilarga yubormoqchisiz?", reply_markup=languagesButton)
        await AdminState.languages.set()
    elif text == "⏮ Amalni bekor qilish":
        await state.finish()
        await message.answer("Hop\n\nNima ish bajaramiz", reply_markup=menu_admin)
    else:
        await message.answer("Tugmalardan biri tanlanishi shart", reply_markup=yesOrNo)
        
@dp.message_handler(state=AdminState.languages)
async def languages(message: types.Message, state=FSMContext):
        i = None   
        text = message.text
        active_users = 0
        deactive_users = 0
        users = None
        if text == "UZ 🇺🇿":
            users = await db.select_all_user_by_lang(language_code='uz')
            i = 'ok'
        elif text == "RU 🇷🇺":
            users = await db.select_all_user_by_lang(language_code='ru')
            i = 'ok'
        elif text == "EN 🏴󠁧󠁢󠁥󠁮󠁧󠁿":
            users = await db.select_all_user_by_lang(language_code='en')
            i = 'ok'
        elif text == "Hamma uchun 📬":
            users = await db.select_all_users()
            i = 'ok'
        
        if i == 'ok':
            if users:
                
                for user in users:
                    user_id = user[3]
                    try:
                        if content_type == 'text':
                            await bot.send_message(chat_id=user_id, text=context)
                        elif content_type == 'photo':
                            await bot.send_photo(photo=file_id, chat_id=user_id, caption=caption if caption else None)
                        elif content_type == 'video':
                            await bot.send_video(video=file_id, chat_id=user_id, caption=caption if caption else None)
                        elif content_type == 'sticker':
                            await bot.send_sticker(chat_id=user_id, sticker=file_id)
                        elif content_type == 'document':
                            await bot.send_document(chat_id=user_id, document=file_id, caption=caption if caption else None)
                        elif content_type == 'poll':
                            await bot.send_poll(chat_id=user_id, question=question, options=options2)
                            
                        active_users += 1
                    except BotBlocked:
                        deactive_users += 1
                    except Exception as e:
                        print(e)
                        pass
                         
                    
                    await asyncio.sleep(0.05)
                    
                await state.finish()
                
                await message.answer(f"Xabar {active_users} ta foydalanuvchiga yuborildi. {deactive_users} ta foydalanuvchi botni bloklab qo'ygan \n\n\nNima ish bajaramiz", reply_markup=menu_admin)
            else:
                await message.answer("Bu til bilan ro'yhatdan o'tganlar yo'q", reply_markup=languagesButton)
        else:
            await message.answer("Tugmalardan biri tanlanishi shart", reply_markup=languagesButton) 
            
@dp.message_handler(state=AdminState.channels)
async def channels(message: types.Message, state=FSMContext):
    text = message.text
    
    if text == "Yangi kanal qo'shish":
        await message.answer("Yangi kanal username sini yuboring", reply_markup=backBtn)
        await AdminState.newChannel.set()
    elif text == "Kanalni o'chirib yuborish":
        await message.answer("O'chirmoqchi bo'lgan kanal username sini yuboring", reply_markup=backBtn)
        await AdminState.delChannel.set()
    elif text == "Kanalni almashtirish":
        await message.answer("Almashtirmoqchi bo'lgan kanalning bazadagi ID sini kiriting", reply_markup=backBtn)
        await AdminState.updateChannel.set()
    else:
        await message.answer("Iltimos tugmalardan birini tanlang")
        
@dp.message_handler(state=AdminState.newChannel)
async def newChannel(message: types.Message, state=FSMContext):
    channelUsername = message.text
    await state.update_data({
        'username': channelUsername 
    })
    try:
        await message.answer("Limit sonini yuboring")
        await AdminState.limitUsers.set()
    except Exception as e:
        print(e)
        
@dp.message_handler(state=AdminState.limitUsers)
async def newChannel(message: types.Message, state=FSMContext):
    try:
        limitUser = int(message.text)
    except:
        await message.answer("Raqam yuboring")
        await AdminState.limitUsers.set()
        
    try:
        data = await state.get_data()
        chat = await bot.get_chat(data['username'])
        
        await db.add_channel(chat.title, data['username'], limitUser)
        await message.answer("Kanal qo'shildi", reply_markup=menu_admin)
        await state.finish()
    except Exception as e:
        await message.answer(f"Kanal qo'shishda xatolik\n\n{e}", reply_markup=menu_admin)
        await state.finish()
    
@dp.message_handler(state=AdminState.delChannel)
async def newChannel(message: types.Message, state=FSMContext):
    channelUsername = message.text
    
    try:
        await db.delete_channel_by_username(channelUsername)
        await message.answer("Kanal o'chirib yuborildi", reply_markup=menu_admin)
        await state.finish()
    except Exception as e:
        print(e)
        
@dp.message_handler(state=AdminState.updateChannel)
async def newChannel(message: types.Message, state=FSMContext):
    channel_id = message.text
    channel_id = int(channel_id)
    try:
        await db.select_channel_by_id(channel_id)
        await message.answer("Yangi kanal username sini yuboring")
        await state.update_data(
            {'id': channel_id}   
        )
        
        await AdminState.update_username.set()
    except Exception as e:
        await message.answer("Bu id bilan bazada saqlangan kanal yo'q", reply_markup=menu_admin)
        print(e)
        await state.finish()
        
@dp.message_handler(state=AdminState.update_username)
async def newChannel(message: types.Message, state=FSMContext):
    newUsername = message.text
    data = await state.get_data()
    id = data.get('id')
    
    try:
        await db.update_channel(newUsername, id)
        await message.answer("Kanal username si yangilandi", reply_markup=menu_admin)
        await state.finish()
    except Exception as e:
        print(e)
        
@dp.message_handler(user_id=ADMINS, text="Mini reklama")
async def mini_ads(message: types.Message):
    await message.answer("Tugmalardan birini tanlang", reply_markup=miniads_keyboards)
    await AdminState.miniads.set()
    
@dp.message_handler(state=AdminState.miniads)
async def miniads(message: types.Message, state=FSMContext):
    text = message.text
    
    if text == "Mini reklama qo'shish":
        await message.answer("Mini reklama matnini yuboring", reply_markup=backBtn)
        await AdminState.newminiad.set()
    elif text == "Mini reklamani o'chirib yuborish":
        await db.update_mini_ads_to_null(id=1)
        await message.answer("Mini reklama o'chirib yuborildi", reply_markup=menu_admin)
        await state.finish()
    elif text == "Mini reklamani almashtirish":
        await message.answer("Yangi mini reklama matnini yuboring", reply_markup=backBtn)
        await AdminState.updateminiad.set()
    else:
        await message.answer("Iltimos tugmalardan birini tanlang")

@dp.message_handler(state=AdminState.newminiad)
async def newMiniAd(message: types.Message, state=FSMContext):
    miniAdText = message.text
    
    try:
        await db.update_mini_ads(text=miniAdText, id=1)
        await message.answer("Yangi reklama qo'shildi", reply_markup=menu_admin)
        await state.finish()
    except Exception as e:
        print(e)

@dp.message_handler(state=AdminState.updateminiad)
async def newMiniAd(message: types.Message, state=FSMContext):
    miniAdText = message.text
    
    try:
        await db.update_mini_ads(text=miniAdText, id=1)
        await message.answer("Reklama matni yangilandi", reply_markup=menu_admin)
        await state.finish()
    except Exception as e:
        print(e)
