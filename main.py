import asyncio

from aiogram import Bot, Dispatcher, F
from app.handlers import router
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config
from aiogram_sqlite_storage.sqlitestore import SQLStorage
from aiogram import Router

from aiogram.fsm.storage.postgresql import PostgreSQLStorage

# Підключення до твоєї бази даних
storage = PostgreSQLStorage(
    dsn=DATABASE_URL,
    table_name="aiogram_fsm"  # можна змінити назву таблиці
)

Config.load()
# storage = SQLStorage("fsm_db.db", serializing_method="json")
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(storage=storage)


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнено!")

