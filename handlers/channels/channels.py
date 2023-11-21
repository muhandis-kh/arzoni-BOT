# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import ChatTypeFilter
# from aiogram.dispatcher.filters import Command
# from aiogram.dispatcher.filters import ContentTypeFilter
# from aiogram.dispatcher.filters import ChatMemberUpdated
# from aiogram.types import ChatType
# from loader import dp

# # @dp.register_chat_member_handler()
# async def on_chat_member_update(message: types.Message):
#     if message.chat.type == ChatType.CHANNEL:
#         if message.new_chat_members:
#             print(message.new_chat_members)
#             # A new user has joined the group
#             for user in message.new_chat_members:
#                 print(f"A new user has joined the group: {user.first_name} ({user.id})")

# # Add the event handler to the dispatcher
# dp.register_message_handler(on_chat_member_update, ChatMemberUpdated())

