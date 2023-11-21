from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_admin = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="REKLAMA"),
        ],
        [
            KeyboardButton(text="Majburiy obuna kanallari ustida amallar")
        ],
        [
            KeyboardButton(text="📊 Statistika")
        ],
        [
            KeyboardButton(text="Obuna bo'lganlar soni")
        ],
        [
            KeyboardButton(text="Mini reklama")
        ],
        
    ],
    resize_keyboard=True
)

verifyBtn = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="✅ Ha"),
            KeyboardButton(text="↩️ Formani qayta to'ldirish"),
        ],
    ],
    resize_keyboard=True
)

languagesButton = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="UZ 🇺🇿"),
            KeyboardButton(text="RU 🇷🇺"),
        ],
        [
            KeyboardButton(text='EN 🏴󠁧󠁢󠁥󠁮󠁧󠁿'),
            KeyboardButton(text='Hamma uchun 📬'),
        ],
        [
            KeyboardButton(text="Bekor qilish"),
        ],
    ],
    resize_keyboard=True
)


backBtn = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="Bekor qilish"),
        ],
    ],
    resize_keyboard=True
)

yesOrNo = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='⏭ Ha'),
            KeyboardButton(text='⏮ Amalni bekor qilish'),
        ],
    ],
    resize_keyboard=True
)

channels_keyboards = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="Yangi kanal qo'shish"),
        ],
        [
            KeyboardButton(text="Kanalni o'chirib yuborish"),
        ],
        [
            KeyboardButton(text='Kanalni almashtirish'),    
        ],
        [
            KeyboardButton(text="Bekor qilish"),
        ]
    ],
    resize_keyboard=True
)

miniads_keyboards = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="Mini reklama qo'shish"),
            KeyboardButton(text="Mini reklamani o'chirib yuborish"),
            KeyboardButton(text='Mini reklamani almashtirish'),
        ],
        [
            KeyboardButton(text="Bekor qilish"),
        ],
    ],
    resize_keyboard=True
)
