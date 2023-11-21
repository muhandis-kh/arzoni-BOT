from aiogram.dispatcher.filters.state import StatesGroup, State

class UserStates(StatesGroup):
    check = State()
    checked = State()