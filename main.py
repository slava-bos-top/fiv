import asyncio
from config import Config

Config.load()

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_sqlite_storage.sqlitestore import SQLStorage

# storage = SQLStorage("fsm_db.db", serializing_method="json")
from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from app.storage import user_phone_map

redis = Redis.from_url(Config.REDIS_URL)

storage = RedisStorage(redis=redis)
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(storage=storage)

from app.handlers import router

async def load_users_from_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    cred_dict = json.loads(Config.GOOGLE_CREDENTIALS)
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/17lcrlxUhcervwQTOctLZkdvBVpAwyuWu7DQQ3d_oVSQ/edit?usp=sharing"
    ).sheet1

    # Колонка 4 - телефон, колонка 5 - user_id
    phones = sheet.col_values(4)
    user_ids = sheet.col_values(5)

    for phone, user_id in zip(phones, user_ids):
        if phone and user_id:
            try:
                user_phone_map[int(user_id)] = phone
            except ValueError:
                pass  # пропускаємо заголовок або порожні рядки

    print(f"✅ Завантажено {len(user_phone_map)} користувачів з таблиці")


async def main():
    dp.include_router(router)
    await load_users_from_sheet()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнено!")

