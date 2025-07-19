from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.command import CommandObject
from aiogram.types import (
    Message,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ReplyKeyboardRemove,
    MenuButtonCommands,
    MenuButtonDefault,
    BotCommandScopeDefault,
    BotCommandScopeChat,
    BotCommand,
)
from aiogram import Router, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramBadRequest
import json

import sys
import base64
import requests

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from app.storage import user_phone_map

with open("lessons.json", "r", encoding="utf-8") as f:
    LESSONS = json.load(f)

router = Router()

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from config import Config
from main import bot


class UserProgress(StatesGroup):
    ends = State()
    go = State()
    way = State()
    kof = State()
    les = State()
    num = State()
    explat = State()
    imgCr = State()
    marafonskey0 = State()
    wek0 = State()
    wek1 = State()
    wek2 = State()
    wek3 = State()
    wek4 = State()
    leson0 = State()
    lesonForWeekSecond0 = State()
    lesonForWeekThird0 = State()
    leson1 = State()
    lesonForWeekSecond1 = State()
    lesonForWeekThird1 = State()
    leson2 = State()
    lesonForWeekSecond2 = State()
    lesonForWeekThird2 = State()
    leson3 = State()
    lesonForWeekSecond3 = State()
    lesonForWeekThird3 = State()
    leson4 = State()
    num = State()
    first_name = State()
    last_name = State()
    numbers = State()
    SignInSuper = State()


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Курси")],
        [KeyboardButton(text="Марафони")],
        [KeyboardButton(text="Про нас")],
    ],
    resize_keyboard=True,
)


list_for_exsel_lesson = [[0, 7, 13], [19, 25, 31], [37, 44, 51], [56, 62, 68], [74]]

marafons = [
    "Фізика",
    "Хімія",
    "Креативність",
    "Програмування",
    "Новорічний",
    "Повернутися до тижнів",
]
weeks = ["Тиждень 1", "Тиждень 2", "Тиждень 3"]
lessons = ["Урок 1", "Урок 2", "Урок 3", "Урок 4", "Урок 5", "Урок 6", "Урок 7"]


# callback
@router.callback_query(F.data == "Done")
async def homework_done_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Прогрес зберігається...")
    data = await state.get_data()
    les = data.get("les", [])

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

    phone_column = sheet.col_values(4)
    number_to_find = user_phone_map.get(callback.from_user.id)

    try:
        row_index = phone_column.index(number_to_find) + 1
        row_values = sheet.row_values(row_index)

        current_module = sys.modules[__name__]

        if les[1] == 0:
            leson_list_name = f"leson{les[0]}"
            lesson_keyboard_name = f"lesson{les[0]}"
        elif les[1] == 1:
            leson_list_name = f"lesonForWeekSecond{les[0]}"
            lesson_keyboard_name = f"lessonForWeekSecond{les[0]}"
        else:
            leson_list_name = f"lesonForWeekThird{les[0]}"
            lesson_keyboard_name = f"lessonForWeekThird{les[0]}"

        # leson_list = getattr(current_module, leson_list_name)
        data = await state.get_data()
        inf = data.get(leson_list_name, [])

        if "✅" in inf[les[2]]:
            # leson_list[les[2]] = f"{leson_list[les[2]]}"
            await callback.message.answer("Цей урок вже було пройдено")
        else:
            # leson_list[les[2]] = f"{leson_list[les[2]]} ✅"
            row_values[25 + list_for_exsel_lesson[les[0]][les[1]] + les[2]] = 1

            sheet.update(f"A{row_index}", [row_values])

            data = await state.get_data()
            l = data.get(leson_list_name, [])
            l[les[2]] = f"{l[les[2]]} ✅"
            await state.update_data(**{leson_list_name: l})
        data = await state.get_data()
        leson_list = data.get(leson_list_name, [])

        lessonKeyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=lesson)] for lesson in leson_list],
            resize_keyboard=True,
        )

        g = 1
        for i in leson_list:
            if i[-1:] == "✅":
                g += 1
        week_list = []
        if int(len(leson_list)) == g:
            wek_list_name = f"wek{les[0]}"
            # week_keyboard_name = f"week{les[0]}"

            data = await state.get_data()
            inf = data.get(wek_list_name, [])

            # week_list = getattr(current_module, wek_list_name)
            if "✅" in inf[les[1]]:
                # week_list[les[1]] = f"{week_list[les[1]]}"
                pass
            else:
                # week_list[les[1]] = f"{week_list[les[1]]} ✅"
                data = await state.get_data()
                l = data.get(wek_list_name, [])
                l[les[1]] = f"{l[les[1]]} ✅"
                await state.update_data(**{wek_list_name: l})
            data = await state.get_data()
            week_list = data.get(wek_list_name, [])

            # setattr(
            #     current_module,
            #     week_keyboard_name,
            #     ReplyKeyboardMarkup(
            #         keyboard=[[KeyboardButton(text=week)] for week in week_list],
            #         resize_keyboard=True,
            #     ),
            # )
            row_values[12 + les[0] * 3 + les[1]] = g

            sheet.update(f"A{row_index}", [row_values])
        j = 1
        if int(len(week_list)) == 0:
            pass
        else:
            for i in week_list:
                if i[-1:] == "✅":
                    j += 1
            if int(len(week_list)) == j:
                mar = "marafonskey0"
                # mar_keyboard_name = "marafonskey"

                # mar_list = getattr(current_module, mar)

                data = await state.get_data()
                inf = data.get(mar, [])

                if "✅" in inf[les[0]]:
                    # mar_list[les[0]] = f"{mar_list[les[0]]}"
                    pass
                else:
                    # mar_list[les[0]] = f"{mar_list[les[0]]} ✅"
                    data = await state.get_data()
                    l = data.get(mar, [])
                    l[les[0]] = f"{l[les[0]]} ✅"
                    await state.update_data(**{mar: l})

                # setattr(
                #     current_module,
                #     mar_keyboard_name,
                #     ReplyKeyboardMarkup(
                #         keyboard=[[KeyboardButton(text=mar)] for mar in mar_list],
                #         resize_keyboard=True,
                #     ),
                # )
                row_values[7 + les[0]] = j

                sheet.update(f"A{row_index}", [row_values])
        data = await state.get_data()
        ends = data.get("ends", [])
        if ends == 0:
            text = (
                "Молодець! Так тримати! Обирай наступний урок! Далі - ще цікавіше! 🙌"
            )
        elif ends == 1:
            text = "Молодець! Так тримати! Обирай наступний тиждень! Далі - ще цікавіше! 🙌"
        else:
            text = "Молодець! Так тримати! Обирай інший марафон або курс! Далі - ще цікавіше! 🙌"
        await callback.message.answer(text=text, reply_markup=lessonKeyboard)
    except ValueError as v:
        if "None is not in list" in str(v):
            await callback.message.answer(
                "Щоб отримати можливість зберігати прогрес, треба зареєструватись або увійти в акаунт",
                reply_markup=kb.regestration,
            )


@router.callback_query(F.data == "comfirmsignIn")
async def homework_done_callbacks(callback: CallbackQuery):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    cred_json_str = Config.GOOGLE_CREDENTIALS

    cred_dict = json.loads(cred_json_str)
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/17lcrlxUhcervwQTOctLZkdvBVpAwyuWu7DQQ3d_oVSQ/edit?usp=sharing"
    ).sheet1

    phone_column = sheet.col_values(4)
    number_to_find = user_phone_map.get(callback.from_user.id)

    row_index = phone_column.index(number_to_find) + 1
    row_values = sheet.row_values(row_index)

    row_values[5] = 1

    sheet.update(f"A{row_index}", [row_values])
    await callback.message.answer("Вхід пітверджено!")


@router.callback_query(F.data == "Молодець! Так тримати!")
async def homework_done_callback(callback: CallbackQuery):
    await callback.answer("Молодець! Так тримати! ✅", show_alert=True)


@router.callback_query(F.data == "explation")
async def homework_done_callbacktask(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    explat = data.get("explat", [])
    imgCr = data.get("imgCr", [])
    image = FSInputFile(imgCr[0])
    await callback.message.answer_photo(
        caption=f"{explat[0]}", photo=image, parse_mode="HTML"
    )


@router.message(CommandStart(deep_link=True))
async def start_handler(message: Message, state: FSMContext, command: CommandObject):
    chat_id = message.chat.id
    user = message.from_user

    # Зберігаємо імʼя/прізвище
    await state.update_data(first_name=[user.first_name])
    await state.update_data(last_name=[user.last_name])

    # Отримуємо deep link параметр
    param = command.args  # Це буде 'confirm_380501234567' або None

    if param and param.startswith("confirm_"):
        phone = param.replace("confirm_", "")
        await state.set_state(UserProgress.numbers)
        await state.update_data(num=[phone])

        await message.answer(
            "👋 Вітаю! Надішліть посилання з номером, для підтвердження номера.",
            reply_markup=kb.get_number,
        )
        print(f"✅ Deep link підтвердження: {phone}")
    else:
        # Стандартна логіка /start без параметрів
        await message.answer("Виникла проблема, повторіть авторизацію")


from cloudinary import uploader, config as cloudinary_config


@router.message(StateFilter(UserProgress.numbers), F.contact)
async def register_city(message: Message, state: FSMContext):
    await message.answer("Дані зберігаються...", reply_markup=ReplyKeyboardRemove())
    await state.update_data(numbers=message.contact)
    data = await state.get_data()
    number = list(data["numbers"])[0][1]

    # 🔐 Google Sheets авторизація
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    cred_json_str = Config.GOOGLE_CREDENTIALS
    cred_dict = json.loads(cred_json_str)
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/17lcrlxUhcervwQTOctLZkdvBVpAwyuWu7DQQ3d_oVSQ/edit?usp=sharing"
    )
    sheet = spreadsheet.sheet1

    # 📸 Завантаження аватарки користувача в Cloudinary
    cloudinary_config(
        cloud_name=Config.CLOUDINARY_CLOUD_NAME,
        api_key=Config.CLOUDINARY_API_KEY,
        api_secret=Config.CLOUDINARY_API_SECRET,
    )

    user_id = message.from_user.id
    photo_url = "0"  # запасне фото

    try:
        photos = await bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            photo = photos.photos[0][-1]
            file = await bot.get_file(photo.file_id)
            file_path = file.file_path
            tg_file_url = (
                f"https://api.telegram.org/file/bot{Config.BOT_TOKEN}/{file_path}"
            )
            response = requests.get(tg_file_url)

            cloudinary_response = uploader.upload(response.content)
            photo_url = cloudinary_response.get("secure_url", photo_url)
    except Exception as e:
        print("❌ Помилка завантаження фото:", e)

    # 🧠 Далі логіка звірки номера
    number = number.replace("(", "").replace(")", "").replace(" ", "").replace("+", "")
    num = data.get("num", [])[0]
    first_name = data.get("first_name", [""])[0]
    last_name = data.get("last_name", [""])[0]

    if number == str(num):
        ena = 0
        phone = number
        user_phone_map[user_id] = phone
        conf = "Confirmed"
        user_data = [
            conf,
            first_name,
            last_name,
            num,
            user_id,
            ena,
            photo_url,
        ]
        user_data += [0] * 99
        sheet.append_row(user_data)
        await message.answer(
            "Номер підтверджено. Вітаємо в клубі розумників та розумниць! 😉"
        )
        await bot.set_my_commands(
            [BotCommand(command="menu", description="Показати меню")],
            scope=BotCommandScopeChat(chat_id=message.chat.id),
        )
        await message.answer(
            "Привіт! Вітаємо тебе в боті FivOne. Тут зібрані курси та марафони, які створила команда спеціалістів і які допоможуть тобі опанувати нові знання легко, цікаво та весело!",
            reply_markup=main,
        )
        await message.answer(
            "Натискай кнопку Меню (на телефоні - три рисочки внизу зліва). Ця кнопка завжди повертатиме тебе до Головного меню. Обирай марафон чи курс, який тебе зацікавив, ознайомлюйся з матеріалами уроку, виконуй завдання та дивуй своїми новими знаннями оточуючих! Запрошуй друзів приєднатися, адже разом дізнаватися щось нове завжди цікавіше! Починаймо! \n👇",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
    else:
        await message.answer("Номер не співпадає з вказаним при реєстрації.")
        await state.clear()


@router.message(Command("start"))
async def regular_start_handler(message: Message, state: FSMContext):
    await bot.set_my_commands(
        [
            BotCommand(command="menu", description="Показати меню"),
        ],
        scope=BotCommandScopeChat(chat_id=message.chat.id),
    )
    await message.answer(
            "Привіт! Вітаємо тебе в боті FivOne. Тут зібрані курси та марафони, які створила команда спеціалістів і які допоможуть тобі опанувати нові знання легко, цікаво та весело!",
            reply_markup=main,
        )
    await message.answer(
        "Натискай кнопку Меню (на телефоні - три рисочки внизу зліва). Ця кнопка завжди повертатиме тебе до Головного меню. Обирай марафон чи курс, який тебе зацікавив, ознайомлюйся з матеріалами уроку, виконуй завдання та дивуй своїми новими знаннями оточуючих! Запрошуй друзів приєднатися, адже разом дізнаватися щось нове завжди цікавіше! Починаймо! \n👇",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("menu"))
async def start(message: Message, state: FSMContext):
    data = await state.get_data()
    go = data.get("go", [])
    if go != True:
        await state.update_data(
            ends=0,
            go=True,
            kof=[0],
            les=[],
            num=[],
            way=[],
            explat=[],
            imgCr=[],
            marafonskey0=[
                "Фізика",
                "Хімія",
                "Креативність",
                "Програмування",
                "Новорічний",
                "Повернутися до головного меню",
            ],
            wek0=[
                "Марафон з фізики. Тиждень 1",
                "Марафон з фізики. Тиждень 2",
                "Марафон з фізики. Тиждень 3",
                "Повернутися до марафонів",
            ],
            wek1=[
                "Марафон з хімії. Тиждень 1",
                "Марафон з хімії. Тиждень 2",
                "Марафон з хімії. Тиждень 3",
                "Повернутися до марафонів",
            ],
            wek2=[
                "Марафон з креативності. Тиждень 1",
                "Марафон з креативності. Тиждень 2",
                "Марафон з креативності. Тиждень 3",
                "Повернутися до марафонів",
            ],
            wek3=[
                "Марафон з IT. Тиждень 1",
                "Марафон з IT. Тиждень 2",
                "Марафон з IT. Тиждень 3",
                "Повернутися до марафонів",
            ],
            wek4=["Наворічний марафон. Тиждень 1", "Повернутися до марафонів"],
            leson0=[
                "Урок 1. Сила Всесвітнього тяжніння. Невагомість",
                "Урок 2. Вільне падіння. Прискорення вільного падіння",
                "Урок 3. Центр мас",
                "Урок 4. Прості механізми",
                "Урок 5. Пружність",
                "Урок 6. Тертя",
                'Урок 7. Додаткове відео "Чому небо блакитне?"',
                "Повернутися до тижнів",
            ],
            lesonForWeekSecond0=[
                "Урок 1. Температура",
                "Урок 2. Енергія",
                "Урок 3. Двигуни",
                "Урок 4. Густина",
                "Урок 5. Тиск",
                "Урок 6. Горіння",
                "Повернутися до тижнів",
            ],
            lesonForWeekThird0=[
                "Урок 1. Електрика",
                "Урок 2. Лампочка",
                "Урок 3. Магніти",
                "Урок 4. Оптика",
                "Урок 5. Зв'язок",
                "Урок 6. Астрофізика",
                "Повернутися до тижнів",
            ],
            leson1=[
                "Урок 1. Явища навколо нас",
                "Урок 2. Періодична система Менделєєва",
                "Урок 3. Речовини та їхні властивості",
                "Урок 4. Атоми, молекули, йони. Маса",
                "Урок 5. Речовини (частина 2)",
                "Урок 6. Суміші та їхні властивості",
                "Повернутися до тижнів",
            ],
            lesonForWeekSecond1=[
                "Урок 1. Суміші (частина 2)",
                "Урок 2. Прості та складні речовини",
                "Урок 3. Валентність. Формули речовин",
                "Урок 4. Закон збереження маси",
                "Урок 5. Органічні речовини",
                "Урок 6. Експерименти",
                "Повернутися до тижнів",
            ],
            lesonForWeekThird1=[
                "Урок 1. Оксиди (Неорганічні речовини)",
                "Урок 2. Кислоти (Неорганічні речовини)",
                "Урок 3. Основи. Індикатори",
                "Урок 4. Солі",
                "Урок 5. Чому речовини мають різний колір?",
                "Урок 6. Підсумок марафону з хімії",
                "Повернутися до тижнів",
            ],
            leson2=[
                "Урок 1. Що таке креативність?",
                "Урок 2. Як шукати нові ідеї?",
                "Урок 3. Чому потрібно фантазувати?",
                "Урок 4. Чи поєднуються креативність та розум?",
                "Урок 5. Які риси мають креативні люди?",
                "Урок 6. Фантазійний календар",
                "Урок 7. Основи дизайну. Ресурси",
                "Повернутися до тижнів",
            ],
            lesonForWeekSecond2=[
                "Урок 1. Що робити, якщо немає ідей?",
                "Урок 2. Мистецтво та Творчість",
                "Урок 3. Музика та креативність",
                "Урок 4. Як театр розвиває креативність?",
                "Урок 5. Креативність в інших видах мистецтва",
                "Урок 6. Шукаємо натхнення навколо нас",
                "Урок 7. Сучасний дизайн. Приклади",
                "Повернутися до тижнів",
            ],
            lesonForWeekThird2=[
                "Урок 1. Мрії та візуалізації",
                "Урок 2. Цінності та креативність",
                "Урок 3. Креативність як частина підприємництва",
                "Урок 4. Командна робота у креативній сфері",
                "Урок 5. 10 кроків для створення креативних проектів",
                "Повернутися до тижнів",
            ],
            leson3=[
                "Урок 1. Вступ до програмування",
                "Урок 2. Програмування життєвих ситуацій",
                "Урок 3. Структура програм",
                "Урок 4. Старт програмування. Діалог",
                "Урок 5. Додаємо умови в код",
                "Урок 6. Мотивація",
                "Повернутися до тижнів",
            ],
            lesonForWeekSecond3=[
                "Урок 1. Основи С++. Арифметика",
                "Урок 2. Умови в мові С++",
                "Урок 3. Алгоритми у С++",
                "Урок 4. Цикли у мові С++",
                "Урок 5. Функції. Підключення бібліотек",
                "Урок 6. Мотивація",
                "Повернутися до тижнів",
            ],
            lesonForWeekThird3=[
                "Урок 1. Основи мови Python",
                "Урок 2. Цикли у мові Python",
                "Урок 3. Підключення бібліотек у мові Python",
                "Урок 4. Рядки у мові Python",
                "Урок 5. Основи JavaScript (підготовка до інтенсиву)",
                "Урок 6. Інтенсив JavaScript",
                "Повернутися до тижнів",
            ],
            leson4=[
                "Урок 1. Іграшка з природних матеріалів",
                "Урок 2. Іграшка в техніці канзаши",
                "Урок 3. Новорічна іграшка з солоного тіста",
                "Урок 4. Іграшка з фетру",
                "Урок 5. Квілінг",
                "Урок 6. Три іграшки з фоамірану",
                "Урок 7. Іграшка у техніці декупаж",
                "Повернутися до тижнів",
            ],
        )
    await message.answer("Обирайте марафон чи курс", reply_markup=main)


@router.message(F.text == "Повернутися до головного меню")
async def start(message: Message):
    await message.answer("Обирайте марафон чи курс", reply_markup=main)


@router.message(F.text.in_(["Марафони", "Повернутися до марафонів"]))
async def Task(message: Message, state: FSMContext):
    await state.update_data(num=[])
    await state.update_data(way=[])
    data = await state.get_data()
    marafonskey = data.get("marafonskey0", [])
    lessonKeyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lesson)] for lesson in marafonskey],
        resize_keyboard=True,
    )
    await message.answer(
        "Обирай, будь ласка, марафон, який тебе зацікавив", reply_markup=lessonKeyboard
    )


@router.message(
    F.text.startswith(
        tuple(
            [
                "Фізика",
                "Хімія",
                "Креативність",
                "Програмування",
                "Новорічний",
                "Повернутися до тижнів",
            ]
        )
    )
)
async def Marafons(message: Message, state: FSMContext):
    if "✅" in message.text:
        mes = message.text[:-2]
    else:
        mes = message.text
    for i in marafons:
        if i == str(mes):
            index = marafons.index(i)
    data = await state.get_data()
    way = data.get("way", [])
    way.append(index)
    await state.update_data(way=way)
    if index == 0:
        await message.answer(
            "<b>Привіт-привіт! </b>😄\nВітаємо тебе на Марафоні з фізики.\n\nУ цьому каналі ти отримуватимеш відеолекції та завдання від авторів марафону з освітнього центру FivOne. В кінці кожного відео буде домашнє завдання - експеримент з певної теми фізики. Також текстовий формат лекції для зручності.\n\nНаприкінці кожного уроку тут з'являтиметься опитування за матеріалом уроку ⚡️\n\nТи можеш переглядати відео та виконувати завдання у будь-який зручний для тебе час. \n\nОтже, <b>3-2-1 полеееетіли</b> 🚀",
            parse_mode="HTML",
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Перелік матеріалів",
                        url="https://docs.google.com/document/d/1ldW3nXfz78LBNLe6Lm6owQyTzYpK1RdybqvZve3JeuY/edit?usp=drivesdk",
                    )
                ]
            ]
        )
        await message.answer(
            text="Переглянути перелік необхідних матеріалів для експериментів, можна за посиланням 👇",
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    elif index == 1:
        await message.answer(
            "<b>Привіт-привіт! </b>😄\nВітаємо тебе на Марафоні з хімії.\n\nУ цьому каналі ти отримуватимеш відеолекції та завдання від авторів марафону з освітнього центру FivOne. В кінці кожного відео буде домашнє завдання - експеримент або симуляція з певної теми хімії. Також ти отримуватимеш текстову версію відеолекції для кращого розуміння матеріалу.\n\nНаприкінці кожного уроку тут з'являтиметься опитування за матеріалом уроку ⚡️\n\nТи можеш переглядати відеолекції та виконувати завдання у будь-який зручний для тебе час. \n\nОтже, <b>3-2-1 полеееетіли </b>🚀",
            parse_mode="HTML",
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Перелік матеріалів",
                        url="https://docs.google.com/document/d/1lTgqZk1gTo1tA3iQwMdrlxuustXzRJFW0C9LBmd4Hec/edit?usp=drivesdk",
                    )
                ]
            ]
        )
        await message.answer(
            text="Переглянути перелік необхідних матеріалів для виконання експериментів 👇",
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    elif index == 2:
        await message.answer(
            "<b>Привіт-привіт!</b> 😄\nВітаємо тебе на Марафоні з Креативності.\n\nУ цьому каналі ти отримуватимеш відеолекції та завдання від авторів марафону з освітнього центру FivOne. В кінці кожного відео буде домашнє завдання - на розвиток креативності. \n\nТакож наприкінці кожного уроку тут з'являтиметься опитування за матеріалом уроку ⚡️\n\nТи можеш переглядати відео та виконувати завдання у будь-який зручний для тебе час.  \n\nОтже, <b>3-2-1 починаємо мислити нестандартно</b> ☀️",
            parse_mode="HTML",
        )
    elif index == 3:
        await message.answer(
            "<b>Привіт-привіт! </b>😄\nВітаємо тебе на ІТ марафоні.\n\nУ цьому каналі ти отримуватимеш відеолекції та завдання від авторів марафону з освітнього центру FivOne. Марафон розрахований на три тижні. Неділя - вихідний😉\n\n<b>Важливо:</b>\n1. Жовті слайди у відеолекціях та презентаціях - це практичні або домашні завдання. Основне домашнє завдання з'являтиметься текстом тут в каналі.\n\n2. Наприкінці першого тижня ти отримаєш тест. Пройди його якнайкраще!\n\n3. Ти можеш переглядати відео та виконувати завдання у будь-який зручний для тебе час. Успіху!\n\n<b>Побігли-ии-иии! </b>🏃",
            parse_mode="HTML",
        )
    elif index == 4:
        image = FSInputFile("app/media/marafons/New/mater.jpg")
        await message.answer_photo(
            photo=image,
            caption="<b>Привіт-привіт! </b>😄\nВітаємо тебе на Новорічному марафоні 🎄\n\nУ цьому каналі протягом тижня ти отримуватимеш відеолекції та завдання від авторів марафону з освітнього центру FivOne. У відео будуть показані всі етапи: від приготування матеріалів до виготовлення іграшок.\n\nТакож у деякі дні тут з'являтимуться додаткові відео, в якому лекторка знайомитиме тебе з матеріалами та даватиме цікаві завдання 😉\n\nТи можеш переглядати відео та майструвати іграшки у будь-який зручний для тебе час.\n\nТакож ось файл з переліком всіх матеріалів (https://drive.google.com/file/d/1SAEblqDHBBaXE5SY68NNLal1vsMprbIa/view?usp=sharing), які тобі знадобляться.\n\n😁 Радимо виготовляти іграшки всією сім'єю або разом з друзями, бо так веселіше!\nДілись з друзями інформацією та запрошуй на марафон!\n\n<b>Це буде класний тиждень! </b>⛄️",
            parse_mode="HTML",
        )
    else:
        pass
    data = await state.get_data()
    way = data.get("way", [])
    if way[0] == 5:
        data = await state.get_data()
        les = data.get("les", [])
        await state.update_data(way=[])
        t = les[0]
        await state.update_data(les=[])
        data = await state.get_data()
        way = data.get("way", [])
        way.append(t)
        await state.update_data(way=way)
    else:
        t = way[0]
        await state.update_data(way=[])
        data = await state.get_data()
        way = data.get("way", [])
        way.append(t)
        await state.update_data(way=way)
    await state.update_data(kof=[0])
    data = await state.get_data()
    f = f"wek{t}"
    week = data.get(f, [])
    lessonKeyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lesson)] for lesson in week],
        resize_keyboard=True,
    )
    await message.answer("Обери тиждень", reply_markup=lessonKeyboard)


@router.message(
    F.text.startswith(
        tuple(
            [
                "Марафон з фізики. Тиждень 1",
                "Марафон з фізики. Тиждень 2",
                "Марафон з фізики. Тиждень 3",
                "Марафон з хімії. Тиждень 1",
                "Марафон з хімії. Тиждень 2",
                "Марафон з хімії. Тиждень 3",
                "Марафон з креативності. Тиждень 1",
                "Марафон з креативності. Тиждень 2",
                "Марафон з креативності. Тиждень 3",
                "Марафон з IT. Тиждень 1",
                "Марафон з IT. Тиждень 2",
                "Марафон з IT. Тиждень 3",
                "Наворічний марафон. Тиждень 1",
            ]
        )
    )
)
async def Week(message: Message, state: FSMContext):
    if "✅" in message.text:
        mes = message.text[:-2]
    else:
        mes = message.text
    for i in weeks:
        if i == str(mes)[-9:]:
            index = weeks.index(i)
    data = await state.get_data()
    way = data.get("way", [])
    way.append(index)
    await state.update_data(way=way)
    current_module = sys.modules[__name__]
    if index == 0:
        data = await state.get_data()
        way = data.get("way", [])
        keyboard_name = f"leson{way[0]}"

    elif index == 1:
        data = await state.get_data()
        way = data.get("way", [])
        keyboard_name = f"lesonForWeekSecond{way[0]}"
    else:
        data = await state.get_data()
        way = data.get("way", [])
        keyboard_name = f"lesonForWeekThird{way[0]}"

    data = await state.get_data()
    week = data.get(keyboard_name, [])
    lessonKeyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lesson)] for lesson in week],
        resize_keyboard=True,
    )

    await message.answer("Обери урок", reply_markup=lessonKeyboard)


# tesks
@router.message(
    F.text.startswith(
        tuple(
            [
                "Урок 1",
                "Урок 2",
                "Урок 3",
                "Урок 4",
                "Урок 5",
                "Урок 6",
                "Урок 7",
                "Наступний урок",
            ]
        )
    )
)
async def Lesson(message: Message, state: FSMContext):
    data = await state.get_data()
    kof = data.get("kof", [])
    les = data.get("les", [])
    way = data.get("way", [])
    if kof[0] == 1:
        await state.update_data(way=[])
        data = await state.get_data()
        way = data.get("way", [])
        way.append(les[0])
        way.append(les[1])
        await state.update_data(way=way)
        data = await state.get_data()
        way = data.get("way", [])
    if len(way) != 0:
        # num.append(way[0])
        # num.append(way[1])
        for i in lessons:
            if i == str(message.text[:6]):
                index = lessons.index(i)
        # num.append(index)
        data = await state.get_data()
        way = data.get("way", [])
        await state.update_data(num=[way[0], way[1], index])
    await state.update_data(les=[])
    # data = await state.get_data()
    # les = data.get("les", [])
    # les.append(way[0])
    # les.append(way[1])
    # les.append(index)
    data = await state.get_data()
    way = data.get("way", [])
    await state.update_data(les=[way[0], way[1], index])
    data = await state.get_data()
    num = data.get("num", [])
    lesson = LESSONS[int(num[0])]
    week = lesson[f"week_{int(num[1])}"]
    tesks = week[f"tesks_{int(num[2])}"]
    image = FSInputFile(tesks["image"])
    caption = f"<b>{tesks['text']}</b>"
    await message.answer_photo(photo=image, caption=caption, parse_mode="HTML")
    textVideo = tesks["textVideo"]
    button_text = tesks["button_text"]
    video_url = tesks["video_url"]
    if video_url != "0":
        text = f'<a href="{video_url}">{textVideo}</a>'
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"{button_text}", url=f"{video_url}")]
            ]
        )
        await message.answer(
            text,
            reply_markup=keyboard,
            parse_mode="HTML",
            disable_web_page_preview=False,
        )

    document = tesks["docs"]
    caption = tesks["textDocs"]
    text = f'<a href="{document}">{caption}</a>'
    if document != "0":
        await message.answer(
            text,
            parse_mode="HTML",
            disable_web_page_preview=False,
        )
    dz = tesks["dz"]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Дз зробив!", callback_data="Молодець! Так тримати!"
                )
            ]
        ]
    )
    if "addDzPr" in tesks:
        video = FSInputFile(tesks["addDzPr"])
        await message.answer_document(
            document=video,
            parse_mode="HTML",
        )
    videoExp = tesks["videoExp"]
    imageexp = FSInputFile(tesks["imgExp"])
    if tesks["imgExp"] == "0":
        if tesks["Cite"] == "0":
            try:
                if videoExp != "0":
                    video = FSInputFile(videoExp)
                    await message.answer_video(
                        video,
                        caption=dz,
                        disable_notification=True,
                        parse_mode="HTML",
                    )
                else:
                    await message.answer(
                        dz,
                        parse_mode="HTML",
                    )
            except TelegramBadRequest as e:
                if "caption is too long" in str(e):
                    await message.answer(
                        dz,
                        parse_mode="HTML",
                    )
                    await message.answer_video(
                        video,
                        disable_notification=True,
                    )
                else:
                    raise e
        else:
            text = f"{dz}"
            await message.answer(
                text,
                disable_web_page_preview=False,
                parse_mode="HTML",
            )
    else:
        try:
            await message.answer_photo(
                photo=imageexp,
                caption=dz,
                parse_mode="HTML",
            )
        except TelegramBadRequest as e:
            if "caption is too long" in str(e):
                await message.answer(
                    dz,
                    parse_mode="HTML",
                )
                await message.answer_photo(
                    photo=imageexp,
                )
            else:
                raise e
    if "docDz" in tesks:
        video = FSInputFile(tesks["docDz"])
        await message.answer_document(
            document=video,
            caption='<b>Зроби додаткове завдання "Таблиця цінностей"</b>',
            parse_mode="HTML",
        )
    if "docDzn" in tesks:
        await message.answer(
            text=tesks["docDzn"],
            parse_mode="HTML",
        )
    k = 1
    for i in tesks["test"]:
        if k == 1:
            await message.answer(text="Перевір себе!", parse_mode="HTML")
        test = tesks["test"][f"test_{k}"]
        question = test["question"]
        correct_option_id = test["correct_index"]
        explanation = test["explanation"]
        options = []
        m = 0
        for n in test["options"]:
            options.append(test["options"][m])
            m += 1
        image = FSInputFile(test["img"])
        if str(test["img"]) != "0":
            await message.answer_photo(photo=image)
        if "music" in test:
            if test["music"] != "0":
                video = FSInputFile(test["music"])

                await message.answer_audio(
                    audio=video, caption="Послухай цей фрагмент музики:"
                )
        if str(explanation) == "0":
            if "imgCr" in test:
                await state.update_data(explat=[])
                await state.update_data(imgCr=[])
                data = await state.get_data()
                explat = data.get("explat", [])
                explat.append(test["dop"])
                await state.update_data(explat=explat)
                data = await state.get_data()
                imgCr = data.get("imgCr", [])
                imgCr.append(test["imgCr"])
                await state.update_data(imgCr=imgCr)
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="Отримати пояснення до завдання",
                                callback_data="explation",
                            )
                        ]
                    ]
                )
                await message.answer_poll(
                    question=question,
                    options=options,
                    is_anonymous=False,
                    type="quiz",
                    correct_option_id=correct_option_id,
                    reply_markup=keyboard,
                )
            else:
                await message.answer_poll(
                    question=question,
                    options=options,
                    is_anonymous=False,
                    type="quiz",
                    correct_option_id=correct_option_id,
                )
        else:
            await message.answer_poll(
                question=question,
                options=options,
                is_anonymous=False,
                type="quiz",
                correct_option_id=correct_option_id,
                explanation=explanation,
            )
        k += 1
    if "addDz" in tesks:
        text = tesks["addDz"]
        await message.answer(
            text,
            disable_web_page_preview=False,
            parse_mode="HTML",
        )
    if "addDzn" in tesks:
        text = tesks["addDzn"]
        await message.answer(
            text,
            disable_web_page_preview=False,
            parse_mode="HTML",
        )
    if "addVid" in tesks:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎥 Завантажити відео",
                        url=tesks["addVid"],
                    )
                ]
            ]
        )
        text = f"Відеопояснення до завдання другого тижня на мові С++ https://www.youtube.com/watch?v=njBJMryXkAU"
        await message.answer(
            text=text,
            parse_mode="HTML",
        )

    text = "Перевір себе!"
    if tesks["addVideo"] != "0":
        text = f'<a href="{tesks["addVideo"]}">#Додаткове відео 👇</a>'
        button_text = "Переглянути відео"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"{button_text}", url=f"{video_url}")]
            ]
        )
        await message.answer(
            text,
            reply_markup=keyboard,
            parse_mode="HTML",
            disable_web_page_preview=False,
        )
    data = await state.get_data()
    way = data.get("way", [])
    if int(way[1]) == 0:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"Обрати інший урок", callback_data="next")]
            ]
        )
    elif int(way[1]) == 1:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Обрати інший урок", callback_data="nextsecond"
                    )
                ]
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Обрати інший урок", callback_data="nextthird"
                    )
                ]
            ]
        )
    await state.update_data(kof=[1])
    if tesks["End"] == "0":
        await state.update_data(ends=0)

        await state.update_data(num=[])
        text = "Крокуй далі, тисни кнопку 👇 Пройдений урок отримає позначку ✅ (урок засвоєний)."
    elif tesks["End"] == "1":
        await state.update_data(ends=1)
        await state.update_data(num=[])
        data = await state.get_data()
        way = data.get("way", [])
        p = way[0]
        await state.update_data(way=[])
        data = await state.get_data()
        way = data.get("way", [])
        way.append(p)
        await state.update_data(way=way)
        text = "Це був останній урок цього тижня! Крокуй далі, тисни кнопку 👇 Пройдений урок отримає позначку ✅ (урок засвоєний)."
    else:
        await state.update_data(ends=2)
        text = "Це був останній урок цього марафону! Крокуй далі, тисни кнопку 👇 Пройдений урок отримає позначку ✅ (урок засвоєний)."
        await state.update_data(num=[])
        await state.update_data(way=[])
    button_text = "Позначити як виконаний ✅"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{button_text}", callback_data="Done")]
        ]
    )
    await message.answer(
        text=text,
        reply_markup=keyboard,
    )

