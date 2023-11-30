from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands



async def on_startup(dispatcher):
    await db.create()
    await db.create_table_users()
    await db.create_table_channels()
    await db.details()
    detail = await db.count_details()
    if detail == 0:
        await db.add_detail(active_users=0, deactive_users=0)
    
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)