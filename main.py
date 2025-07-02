import asyncio

from aiogram import Bot, Dispatcher
from app.handlers import router
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, BotCommand, MenuButtonCommands

from config import Config

Config.load()
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@router.message(Command("start"))
async def set_menu_commands(message: Message):
    commands = [
        BotCommand(command="menu", description="Показати меню"),
    ]
    await bot.set_my_commands(commands)
    await bot.set_chat_menu_button(
        chat_id=message.chat.id, menu_button=MenuButtonCommands()
    )
    await message.answer("Привіт!")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнено!")
