from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

random_film = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="🎲 Tasodifiy film")],
    ],
    resize_keyboard=True,
)

random_film_ru = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="🎲 Случайный фильм")],
    ],
    resize_keyboard=True,
)