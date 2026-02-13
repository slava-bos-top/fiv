import asyncio
from config import Config

Config.load()

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_sqlite_storage.sqlitestore import SQLStorage

storage = SQLStorage("fsm_db.db", serializing_method="json")
# from redis.asyncio import Redis
# from aiogram.fsm.storage.redis import RedisStorage

# redis = Redis.from_url(Config.REDIS_URL)

# storage = RedisStorage(redis=redis)
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(storage=storage)

from app.handlers import router


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнено!")

