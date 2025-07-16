import asyncio
import re
import json

from aiogram import Bot, Dispatcher, F
from app.handlers import router
import app.keyboards as kb
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message,
    BotCommand,
    MenuButtonCommands,
    MenuButtonDefault,
    BotCommandScopeDefault,
    BotCommandScopeChat,
    ReplyKeyboardRemove,
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import Config

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import hashlib
import string

from app.storage import user_phone_map

Config.load()
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Register(StatesGroup):
    name = State()
    secondName = State()
    years = State()
    password = State()
    number = State()
    yourNumber = State()
    num = State()
    first_name = State()
    last_name = State()
    numbers = State()


@router.message(CommandStart(deep_link=True))
async def start_handler(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user = message.from_user
    await state.update_data(first_name=[user.first_name])
    await state.update_data(last_name=[user.last_name])
    user_id = message.from_user.id
    text = message.text

    # 🔍 Витягуємо аргумент після /start
    if message.text.startswith("/start "):
        param = message.text.split(" ", 1)[1]  # ← буде "phone_380501234567"

        if param.startswith("phone_"):
            await state.set_state(Register.numbers)
            phone = param.replace("phone_", "")
            await message.answer(
                f"👋 Вітаю! Надішліть посилання з номером, для підтвердження номера.",
                reply_markup=kb.get_number,
            )
            print(f"Chat ID: {chat_id}, Phone: {phone}")
            await state.update_data(num=[phone])
        else:
            await message.answer("❌ Невірний формат параметра.")
    else:
        await message.answer("👋 Вітаю! Надішліть посилання з номером.")


@router.message(StateFilter(Register.numbers), F.contact)
async def register_city(message: Message, state: FSMContext):
    await message.answer("Дані зберігаються...", reply_markup=ReplyKeyboardRemove())
    await state.update_data(numbers=message.contact)
    data = await state.get_data()
    number = list(data["numbers"])[0][1]
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    # creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
    cred_json_str = Config.GOOGLE_CREDENTIALS

    cred_dict = json.loads(cred_json_str)
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/17lcrlxUhcervwQTOctLZkdvBVpAwyuWu7DQQ3d_oVSQ/edit?usp=sharing"
    )

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    # creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
    cred_json_str = Config.GOOGLE_CREDENTIALS

    cred_dict = json.loads(cred_json_str)
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)

    client = gspread.authorize(creds)

    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/17lcrlxUhcervwQTOctLZkdvBVpAwyuWu7DQQ3d_oVSQ/edit?usp=sharing"
    ).sheet1
    phone_column = sheet.col_values(5)

    sheet = spreadsheet.sheet1
    number = number.replace("(", "").replace(")", "").replace(" ", "").replace("+", "")
    data = await state.get_data()
    num = data.get("num", [])
    first_name = data.get("first_name", [])
    last_name = data.get("last_name", [])
    num = num[0]
    if number == str(num):
        phone = number
        user_phone_map[message.from_user.id] = phone
        conf = "Confirmed"
        user_data = [conf, first_name[0], last_name[0], num, message.from_user.id]
        for i in range(0, 99):
            user_data.append(0)
        sheet.append_row(user_data)
        user_data.clear()
        await message.answer(
            "Номер підтверджено. Вітаємо в клубі розумників та розумниць! 😉"
        )
        # await message.answer(
        #     "Залишилось лише увійти у свій акаунт, для цього натисни кнопку нижче",
        #     reply_markup=kb.singIn,
        # )
        await state.clear()
    else:
        await message.answer(
            "Номер на якому знаходиться телеграм не співпадає з номером вказаним при реєстрації",
            reply_markup=kb.singIn,
        )
        await state.clear()

# Увійти
@router.message(F.text == "Увійти в акаунт")
async def register_singin(message: Message, state: FSMContext):
    await state.set_state(Register.yourNumber)
    await message.answer(
        "Відправ свій номер, для цього натисни кнопку знизу",
        reply_markup=kb.get_number,
    )


@router.message(StateFilter(Register.yourNumber), F.contact)
async def register_yornum(message: Message, state: FSMContext):
    await state.update_data(number=message.contact)
    await message.answer("Вхід виконується...", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    number = list(data["number"])[0][1]
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    # creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
    cred_json_str = Config.GOOGLE_CREDENTIALS

    cred_dict = json.loads(cred_json_str)
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/17lcrlxUhcervwQTOctLZkdvBVpAwyuWu7DQQ3d_oVSQ/edit?usp=sharing"
    ).sheet1
    phone_column = sheet.col_values(5)
    number = number.replace("(", "").replace(")", "").replace(" ", "")
    if number in phone_column:
        user_phone_map[message.from_user.id] = number
        await message.answer("Вітаємо! Ви увійшли у свій акаунт!")
        await state.clear()
        await bot.set_my_commands(
            [
                BotCommand(command="menu", description="Показати меню"),
            ],
            scope=BotCommandScopeChat(chat_id=message.chat.id),
        )
        await message.answer(
            "Натискай кнопку Меню (на телефоні - три рисочки внизу зліва). Ця кнопка завжди повертатиме тебе до Головного меню. Обирай марафон чи курс, який тебе зацікавив, ознайомлюйся з матеріалами уроку, виконуй завдання та дивуй своїми новими знаннями оточуючих! Запрошуй друзів приєднатися, адже разом дізнаватися щось нове завжди цікавіше! Починаймо! \n👇",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.update_data(enabled=True)
    else:
        await message.answer(
            "Акаунта з таким номером, на жаль, немає. Спочатку потрібно зареєструватись, для цього натисни кнопку нижче",
            reply_markup=kb.reg,
        )


# Зареєструватись
@router.message(F.text == "Зареєструватись")
async def register_name(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer("Давай знайомитись!", reply_markup=ReplyKeyboardRemove())
    await message.answer("Напиши своє ім'я")


@router.message(Register.name)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.secondName)
    await message.answer("Напиши своє прізвище")


@router.message(Register.secondName)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(secondName=message.text)
    await state.set_state(Register.years)
    await message.answer("Скільки тобі років?")


@router.message(Register.years)
async def register_city(message: Message, state: FSMContext):
    text = message.text.strip()

    if re.fullmatch(r"[1-9]\d?", text):
        await state.update_data(years=message.text)
        await state.set_state(Register.password)
        await message.answer(
            "Придумай пароль, який буде складатись не менше, ніж з 8 символів (цифри та великі літери)"
        )
    else:
        await message.answer("❌ Введи 1 або 2 цифри, без нулів на початку.")


@router.message(Register.password)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(password=message.text)

    allowed_chars = set(string.ascii_letters + string.digits + string.punctuation)

    has_letter = any(c.isalpha() and c in string.ascii_letters for c in message.text)
    has_digit = any(c.isdigit() for c in message.text)
    only_allowed = all(c in allowed_chars for c in message.text)
    upper = any(char.isupper() for char in message.text)

    if only_allowed == True:
        if len(message.text) >= 8:
            if has_letter == True and has_digit == True:
                if upper == True:
                    await state.set_state(Register.number)
                    await message.answer(
                        "Залиш, будь ласка, свій номер телефону, щоб у разі необхідності, ми могли зв'язатися з тобою. Для цього натисни кнопку знизу",
                        reply_markup=kb.get_number,
                    )
                else:
                    await message.answer("Пароль повинен містити велику літеру")
                    await message.answer("Введіть інший пароль")
            else:
                await message.answer("Пароль повинен містити літери й цифри")
                await message.answer("Введіть інший пароль")
        else:
            await message.answer("Пароль повинен містити не менше 8 символів")
            await message.answer("Введіть інший пароль")
    else:
        await message.answer("Пароль повинен містити лише літери з латиниці")
        await message.answer("Введіть інший пароль")


@router.message(StateFilter(Register.number), F.contact)
async def register_city(message: Message, state: FSMContext):
    await message.answer("Дані зберігаються...", reply_markup=ReplyKeyboardRemove())
    await state.update_data(number=message.contact)
    data = await state.get_data()
    number = list(data["number"])[0][1]
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    # creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
    cred_json_str = Config.GOOGLE_CREDENTIALS

    cred_dict = json.loads(cred_json_str)
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/17lcrlxUhcervwQTOctLZkdvBVpAwyuWu7DQQ3d_oVSQ/edit?usp=sharing"
    )

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    # creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
    cred_json_str = Config.GOOGLE_CREDENTIALS

    cred_dict = json.loads(cred_json_str)
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)

    client = gspread.authorize(creds)

    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/17lcrlxUhcervwQTOctLZkdvBVpAwyuWu7DQQ3d_oVSQ/edit?usp=sharing"
    ).sheet1
    phone_column = sheet.col_values(5)

    sheet = spreadsheet.sheet1
    name = data["name"]
    surname = data["secondName"]
    year = data["years"]
    password = data["password"]
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    number = number.replace("(", "").replace(")", "").replace(" ", "")
    if number in phone_column:
        await message.answer(
            "Акаунт з таким номером вже зареєстрован. Увійди у свій акаунт",
            reply_markup=kb.singIn,
        )
        await state.clear()
    else:
        phone = number
        user_phone_map[message.from_user.id] = phone
        user_data = [name, surname, year, hashed_password, phone]
        for i in range(0, 99):
            user_data.append(0)
        sheet.append_row(user_data)
        user_data.clear()
        await message.answer(
            "Реєстрацію завершено. Вітаємо в клубі розумників та розумниць! 😉"
        )
        await message.answer(
            "Залишилось лише увійти у свій акаунт, для цього натисни кнопку нижче",
            reply_markup=kb.singIn,
        )
        await state.clear()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнено!")

