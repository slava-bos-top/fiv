import asyncio

from aiogram import Bot, Dispatcher, F
from app.handlers import router
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config

Config.load()
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнено!")

