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
    BufferedInputFile,
)
from aiogram import Router, F

router = Router()

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramBadRequest
import json

import sys
import base64
import requests

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from app.storage import user_phone_map


from app import storage_json
# with open("lessons.json", "r", encoding="utf-8") as f:
#     LESSONS = json.load(f)

# with open("curs.json", "r", encoding="utf-8") as c:
#     CURS = json.load(c)

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from config import Config

# from main import bot

from io import BytesIO
import matplotlib.pyplot as plt

FREE_ACCESS_MODE = True


class UserProgress(StatesGroup):
    allow = State()
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
    first_name = State()
    last_name = State()
    numbers = State()
    SignInSuper = State()
    statisticM = State()
    dzM = State()
    indexM = State()
    indexWeekM = State()
    # Curs:
    Curskey0 = State()
    Cursnum = State()
    Cursway = State()
    Cursles = State()
    Curskof = State()
    task0 = State()
    task1 = State()
    task2 = State()
    Cursends = State()
    indexC = State()
    dzC = State()
    statisticC = State()
    parts_of_tasks = State()
    last_part = State()
    dzPart = State()
    Exp = State()
    kN = State()


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Курси")],
        [KeyboardButton(text="Марафони")],
        [KeyboardButton(text="Твій прогрес")],
        [KeyboardButton(text="Про нас")],
    ],
    resize_keyboard=True,
)


list_for_exsel_lesson = [[0, 7, 14], [20, 26, 32], [38, 45, 52], [57, 63, 69], [75]]

marafons = [
    "Фізика",
    "Хімія",
    "Креативність",
    "Програмування",
    "Новорічний",
    "Повернутися до тижнів",
]
Curs = [
    "Курс. Розвиток креативності",
    "Курс. Фізика навколо нас",
    "Курс. Старт програмування. Мова С++",
    "Повернутись до занять",
]
weeks = ["Тиждень 1", "Тиждень 2", "Тиждень 3"]
lessons = [
    "Урок 1",
    "Урок 2",
    "Урок 3",
    "Урок 4",
    "Урок 5",
    "Урок 6",
    "Урок 7",
    "Наступ",
    "Перейт",
]

tasks = [
    "Заняття 1.",
    "Заняття 2.",
    "Заняття 3.",
    "Заняття 4.",
    "Заняття 5.",
    "Заняття 6.",
    "Заняття 7.",
    "Заняття 8.",
    "Заняття 9.",
    "Заняття 10",
    "Наступне з",
]

parts_of_task = [
    "Частина 1.",
    "Частина 2.",
    "Частина 3.",
    "Частина 4.",
    "Частина 5.",
    "Частина 6.",
    "Частина 7.",
    "Частина 8.",
    "Частина 9.",
    "Частина 10",
    "Повернутись до занять",
]

# callback

# Curs


@router.callback_query(F.data == "Exp")
async def dz(callback: CallbackQuery, state: FSMContext):
    from main import bot

    data = await state.get_data()
    dzC = data.get("dzC", [])

    t = dzC["explain"]

    text = f'<a href="{t}">Відеопояснення до завдання 5\n#відео 👇</a>'
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Дивитись відеопояснення", url=f"{t}")]
        ]
    )

    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML",
        disable_web_page_preview=False,
    )


@router.callback_query(F.data == "refresh_tasks")
async def handle_refresh_callback(callback: CallbackQuery, state: FSMContext):
    from main import bot

    await callback.answer()

    # Отримуємо необхідні дані
    chat_id = callback.message.chat.id
    user_id = callback.from_user.id
    bot_id = bot.id

    # Створюємо "фейкове" повідомлення
    data = await state.get_data()
    Cursends = data.get("Cursends", [])

    if Cursends == 0:
        fake_msg = Message(
            message_id=9999,
            date=datetime.now(),
            chat=callback.message.chat,
            from_user=callback.from_user,
            text="Наступне заняття",
        )
        await LessonCurs(fake_msg, state)


@router.callback_query(F.data == "refresh_part_tasks")
async def handle_refresh_callback(callback: CallbackQuery, state: FSMContext):
    from main import bot

    await callback.answer()

    # Отримуємо необхідні дані
    chat_id = callback.message.chat.id
    user_id = callback.from_user.id
    bot_id = bot.id

    # Створюємо "фейкове" повідомлення

    data = await state.get_data()
    kN = data.get("kN", [])

    fake_msg = Message(
        message_id=9999,
        date=datetime.now(),
        chat=callback.message.chat,
        from_user=callback.from_user,
        text=f"Частина {kN+2}.",
    )
    await LessonpartCurs(fake_msg, state)


@router.callback_query(F.data == "dzCC")
async def dz(callback: CallbackQuery, state: FSMContext):
    from main import bot

    data = await state.get_data()
    dzC = data.get("dzC", [])
    dzPart = data.get("dzPart", [])

    t = dzPart

    keyboardExplain = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Відповідь на завдання", callback_data="Exp")]
        ]
    )

    if dzPart != "0":
        if "explain" in dzC:
            data = await state.get_data()
            Exp = data.get("Exp", [])
            if Exp == "1":
                await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=t,
                    parse_mode="HTML",
                    disable_web_page_preview=False,
                    reply_markup=keyboardExplain,
                )
            else:
                await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=t,
                    parse_mode="HTML",
                    disable_web_page_preview=False,
                )
        else:
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=t,
                parse_mode="HTML",
                disable_web_page_preview=False,
            )

    data = await state.get_data()
    Cursway = data.get("Cursway", [])

    await state.update_data(Curskof=[1])
    data = await state.get_data()
    last_part = data.get("last_part", [])
    if last_part == 1:
        if dzC["End"] == "0":
            await state.update_data(Cursends=0)
            textForEnds = "Готовий до наступного заняття? 🚀"
            textForEndstextForEndsInButton = "Наступне заняття"
            # await state.update_data(Cursnum=[])
            text = "Крокуй далі, тисни кнопку 👇 Пройдене завдання отримає позначку ✅ (завдання зроблено)."
        elif dzC["End"] == "1":
            await state.update_data(Cursends=1)
            # await state.update_data(Cursnum=[])
            data = await state.get_data()
            Cursway = data.get("Cursway", [])
            p = Cursway[0]
            await state.update_data(Cursway=[])
            data = await state.get_data()
            Cursway = data.get("Cursway", [])
            Cursway.append(p)
            await state.update_data(Cursway=Cursway)
            text = "Це було останнє заняття цього тижня! Крокуй далі, тисни кнопку 👇 Пройдений урок отримає позначку ✅ (урок засвоєний)."
        else:
            await state.update_data(Cursends=2)
            text = "Це було останнє заняття цього курсу! Крокуй далі, тисни кнопку 👇 Пройдене завдання отримає позначку ✅ (завдання зроблено)."
            await state.update_data(Cursnum=[])
            await state.update_data(Cursway=[])
        button_text = "Позначити як виконаний ✅"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"{button_text}", callback_data="CursDone")]
            ]
        )

        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

        if dzC["End"] != "2":
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=textForEndstextForEndsInButton,
                            callback_data="refresh_tasks",
                        )
                    ]
                ]
            )
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=textForEnds,
                reply_markup=keyboard,
            )
        else:
            data = await state.get_data()
            Curskey0 = data.get("Curskey0", [])
            lessonKeyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=lesson)] for lesson in Curskey0],
                resize_keyboard=True,
            )
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text="Вітаю, ти завершив курс! 🔥 Готовий до нового виклику? Обери наступний!",
                reply_markup=lessonKeyboard,
            )
    else:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text="Вітаю, ти завершив цю частину заняття! Обери наступну!",
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Наступна частина заняття",
                        callback_data="refresh_part_tasks",
                    )
                ]
            ]
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text="Готовий до наступної частини заняття? 🚀",
            reply_markup=keyboard,
        )
    await state.update_data(last_part=0)


# Marafons

from datetime import datetime


@router.callback_query(F.data == "refresh_lessons")
async def handle_refresh_callback(callback: CallbackQuery, state: FSMContext):
    from main import bot

    await callback.answer()

    # Отримуємо необхідні дані
    chat_id = callback.message.chat.id
    user_id = callback.from_user.id
    bot_id = bot.id

    # Створюємо "фейкове" повідомлення
    data = await state.get_data()
    ends = data.get("ends", [])

    if ends == 0:
        fake_msg = Message(
            message_id=9999,
            date=datetime.now(),
            chat=callback.message.chat,
            from_user=callback.from_user,
            text="Наступний урок",
        )
        await LessonMAR(fake_msg, state)
    elif ends == 1:
        fake_msg = Message(
            message_id=9999,
            date=datetime.now(),
            chat=callback.message.chat,
            from_user=callback.from_user,
            text="Перейти на наступний тиждень",
        )
        await LessonMAR(fake_msg, state)
    else:
        pass


@router.callback_query(F.data == "dzMM")
async def dz(callback: CallbackQuery, state: FSMContext):
    from main import bot

    data = await state.get_data()
    tesks = data.get("dzM", [])
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
        await bot.send_document(
            chat_id=callback.message.chat.id,
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
                    await bot.send_video(
                        chat_id=callback.message.chat.id,
                        video=video,
                        caption=dz,
                        disable_notification=True,
                        parse_mode="HTML",
                    )
                else:
                    await bot.send_message(
                        chat_id=callback.message.chat.id,
                        text=dz,
                        parse_mode="HTML",
                    )
            except TelegramBadRequest as e:
                if "caption is too long" in str(e):
                    await bot.send_message(
                        chat_id=callback.message.chat.id,
                        text=dz,
                        parse_mode="HTML",
                    )
                    await bot.send_video(
                        chat_id=callback.message.chat.id,
                        video=video,
                        disable_notification=True,
                    )
                else:
                    raise e
        else:
            text = f"{dz}"
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=text,
                disable_web_page_preview=False,
                parse_mode="HTML",
            )
    else:
        try:
            await bot.send_photo(
                chat_id=callback.message.chat.id,
                photo=imageexp,
                caption=dz,
                parse_mode="HTML",
            )
        except TelegramBadRequest as e:
            if "caption is too long" in str(e):
                await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=dz,
                    parse_mode="HTML",
                )
                await bot.send_photo(
                    chat_id=callback.message.chat.id,
                    photo=imageexp,
                )
            else:
                raise e
    if "docDz" in tesks:
        video = FSInputFile(tesks["docDz"])
        await bot.send_document(
            chat_id=callback.message.chat.id,
            document=video,
            caption='<b>Зроби додаткове завдання "Таблиця цінностей"</b>',
            parse_mode="HTML",
        )
    if "docDzn" in tesks:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=tesks["docDzn"],
            parse_mode="HTML",
        )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Перевірити себе", callback_data="check")]
        ]
    )
    data = await state.get_data()
    tesks = data.get("dzM", [])
    ggg = 1
    if len(tesks["test"]) == 0:
        if "addDz" not in tesks:
            if "addDzn" not in tesks:
                if "addVid" not in tesks:
                    if tesks["addVideo"] == "0":
                        ggg = 0

    if ggg == 1:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text="Готовий перевірити себе? Натисни кнопку нижче 👇 та вперед!",
            reply_markup=keyboard,
        )
    else:
        ggg = 1
        data = await state.get_data()
        way = data.get("way", [])
        if int(way[1]) == 0:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=f"Обрати інший урок", callback_data="next"
                        )
                    ]
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
            textForEnds = "Готовий до наступного уроку? 🚀"
            textForEndstextForEndsInButton = "Наступний урок"
        elif tesks["End"] == "1":
            textForEnds = "Новий тиждень — нові знання! 🚀"
            textForEndstextForEndsInButton = "Наступний тиждень"
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
            textForEnds = "Обирай інший марафон"
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
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

        if tesks["End"] != "2":
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=textForEndstextForEndsInButton,
                            callback_data="refresh_lessons",
                        )
                    ]
                ]
            )
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=textForEnds,
                reply_markup=keyboard,
            )
        else:
            data = await state.get_data()
            marafonskey = data.get("marafonskey0", [])
            lessonKeyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=lesson)] for lesson in marafonskey],
                resize_keyboard=True,
            )
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text="Вітаю, ти завершив марафон! 🔥 Готовий до нового виклику? Обери наступний!",
                reply_markup=lessonKeyboard,
            )


@router.callback_query(F.data == "check")
async def dz(callback: CallbackQuery, state: FSMContext):
    from main import bot

    data = await state.get_data()
    tesks = data.get("dzM", [])
    dz = tesks["dz"]
    k = 1
    # Додати повідомлення Цього разу без тестів — просто насолоджуйся матеріалом!
    # if len(tesks["test"]) == 0:
    #     await bot.send_message(
    #         chat_id=callback.message.chat.id,
    #         text="Цього разу без тестів — просто насолоджуйся матеріалом!",
    #     )
    for i in tesks["test"]:
        if k == 1:
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text="Перевір себе!",
                parse_mode="HTML",
            )
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
            await bot.send_photo(chat_id=callback.message.chat.id, photo=image)
        if "music" in test:
            if test["music"] != "0":
                video = FSInputFile(test["music"])
                await bot.send_audio(
                    chat_id=callback.message.chat.id,
                    audio=video,
                    caption="Послухай цей фрагмент музики:",
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
                await bot.send_poll(
                    chat_id=callback.message.chat.id,
                    question=question,
                    options=options,
                    is_anonymous=False,
                    type="quiz",
                    correct_option_id=correct_option_id,
                    reply_markup=keyboard,
                )
            else:
                await bot.send_poll(
                    chat_id=callback.message.chat.id,
                    question=question,
                    options=options,
                    is_anonymous=False,
                    type="quiz",
                    correct_option_id=correct_option_id,
                )
        else:
            await bot.send_poll(
                chat_id=callback.message.chat.id,
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
        if "videoExpAdd" in tesks:
            videoExpAdd = tesks["videoExpAdd"]
            video = FSInputFile(videoExpAdd)
            await bot.send_video(
                chat_id=callback.message.chat.id,
                video=video,
                caption=text,
                disable_notification=True,
                parse_mode="HTML",
            )
        else:
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=text,
                disable_web_page_preview=False,
                parse_mode="HTML",
            )
    if "addDzn" in tesks:
        text = tesks["addDzn"]
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
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
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            parse_mode="HTML",
        )

    text = "Перевір себе!"
    if tesks["addVideo"] != "0":
        text = f'<a href="{tesks["addVideo"]}">#Додаткове відео 👇</a>'
        video_url = tesks["addVideo"]
        button_text = "Переглянути відео"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"{button_text}", url=f"{video_url}")]
            ]
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
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
        textForEnds = "Готовий до наступного уроку? 🚀"
        textForEndstextForEndsInButton = "Наступний урок"
    elif tesks["End"] == "1":
        textForEnds = "Новий тиждень — нові знання! 🚀"
        textForEndstextForEndsInButton = "Наступний тиждень"
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
        textForEnds = "Обирай інший марафон"
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
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    if tesks["End"] != "2":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=textForEndstextForEndsInButton,
                        callback_data="refresh_lessons",
                    )
                ]
            ]
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=textForEnds,
            reply_markup=keyboard,
        )
    else:
        data = await state.get_data()
        marafonskey = data.get("marafonskey0", [])
        lessonKeyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=lesson)] for lesson in marafonskey],
            resize_keyboard=True,
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text="Вітаю, ти завершив марафон! 🔥 Готовий до нового виклику? Обери наступний!",
            reply_markup=lessonKeyboard,
        )


@router.callback_query(F.data == "Done")
async def homework_done_callback(callback: CallbackQuery, state: FSMContext):
    if FREE_ACCESS_MODE == False:
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
            await callback.message.answer("Цей урок вже було пройдено!")
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

        data = await state.get_data()
        statisticM = data.get("statisticM", [])
        g = 1
        for i in leson_list:
            if i[-1:] == "✅":
                g += 1
        statisticM[les[0]][les[1]] = g - 1
        await state.update_data(statisticM=statisticM)
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
        row_values[12 + les[0] * 3 + les[1]] = g - 1

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
            row_values[7 + les[0]] = j - 1

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
            if FREE_ACCESS_MODE:
                await callback.message.answer(
                    text="<b>Зараз йде доробка функції збереження прогресу. Ця функція буде доступна через декілька днів. Коли функція буде додана Вам прийде лист, де потрібно буде зареєструватись на сайті, після чого Ви отримаєте можливість зберігати прогрес!</b>",
                    parse_mode="HTML"
                )
            else:
                await callback.message.answer(
                    "Щоб зберігати свій прогрес зареєструйся на сайті (https://fivone.education/). Після реєстрації зможеш спостерігати за своїм прогресом ти зможеш в особистому профілі на сайті або в боті.",
                )


# Curs


@router.callback_query(F.data == "CursDone")
async def homework_done_callback(callback: CallbackQuery, state: FSMContext):
    if FREE_ACCESS_MODE == False:
        await callback.message.answer("Прогрес зберігається...")
    data = await state.get_data()
    Cursles = data.get("Cursles", [])

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

        if Cursles[0] == 0:
            leson_list_name = f"task{Cursles[0]}"
            lesson_keyboard_name = f"lesson{Cursles[0]}"
        elif Cursles[0] == 1:
            leson_list_name = f"task{Cursles[0]}"
            lesson_keyboard_name = f"lessonForWeekSecond{Cursles[0]}"
        else:
            leson_list_name = f"task{Cursles[0]}"
            lesson_keyboard_name = f"lessonForWeekThird{Cursles[0]}"

        # leson_list = getattr(current_module, leson_list_name)
        data = await state.get_data()
        inf = data.get(leson_list_name, [])

        if "✅" in inf[Cursles[1]]:
            await callback.message.answer("Це завдання вже було пройдено!")
        else:
            # Зберігаємо галочку в Google Sheets
            col_index = 109 + Cursles[0] * 10 + Cursles[1]
            # Розширюємо рядок якщо потрібно
            while len(row_values) <= col_index:
                row_values.append(0)
            row_values[col_index] = 1
            sheet.update(f"A{row_index}", [row_values])

            data = await state.get_data()
            l = data.get(leson_list_name, [])
            l[Cursles[1]] = f"{l[Cursles[1]]} ✅"
            await state.update_data(**{leson_list_name: l})
        data = await state.get_data()
        leson_list = data.get(leson_list_name, [])

        lessonKeyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=lesson)] for lesson in leson_list],
            resize_keyboard=True,
        )

        data = await state.get_data()
        statisticC = data.get("statisticC", [])

        g = 1
        for i in leson_list:
            if i[-1:] == "✅":
                g += 1
        statisticC[Cursles[0]][0] = g - 1
        await state.update_data(statisticC=statisticC)
        week_list = []
        if int(len(leson_list)) == g:
            wek_list_name = f"Curskey0"
            # week_keyboard_name = f"week{les[0]}"

            data = await state.get_data()
            inf = data.get(wek_list_name, [])

            # week_list = getattr(current_module, wek_list_name)
            if "✅" in inf[Cursles[0]]:
                # week_list[les[1]] = f"{week_list[les[1]]}"
                pass
            else:
                # week_list[les[1]] = f"{week_list[les[1]]} ✅"
                data = await state.get_data()
                l = data.get(wek_list_name, [])
                l[Cursles[0]] = f"{l[Cursles[0]]} ✅"
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
        row_values[105 + Cursles[0]] = g - 1

        sheet.update(f"A{row_index}", [row_values])
        data = await state.get_data()
        ends = data.get("Cursends", [])
        if ends == 0:
            text = "Молодець! Так тримати! Обирай наступне завдання! Далі - ще цікавіше! 🙌"
        elif ends == 1:
            text = "Молодець! Так тримати! Обирай наступний тиждень! Далі - ще цікавіше! 🙌"
        else:
            text = "Молодець! Так тримати! Обирай інший марафон або курс! Далі - ще цікавіше! 🙌"
        await callback.message.answer(text=text, reply_markup=lessonKeyboard)
    except ValueError as v:
        if "None is not in list" in str(v):
            if FREE_ACCESS_MODE:
                await callback.message.answer(
                    text="<b>Зараз йде доробка функції збереження прогресу. Ця функція буде доступна через декілька днів. Коли функція буде додана Вам прийде лист, де потрібно буде зареєструватись на сайті, після чого Ви отримаєте можливість зберігати прогрес!</b>",
                    parse_mode="HTML"
                )
            else:
                await callback.message.answer(
                    "Cпостерігати за своїм прогресом ти зможеш в особистому профілі на сайті https://fivone.education/ (якщо ще не авторизувався - саме час це зробити😉).",
                )


@router.callback_query(F.data == "comfirmsignIn")
async def homework_done_callbacks(callback: CallbackQuery, state: FSMContext):
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
    await state.update_data(allow=[1])
    await callback.message.answer(
        "Вхід пітверджено! Натискай Меню!", reply_markup=ReplyKeyboardRemove()
    )


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
            "👋 Підтверджуй номер телефону й отримуй доступ до курсів та марафонів!",
            reply_markup=kb.get_number,
        )
        print(f"✅ Deep link підтвердження: {phone}")
    else:
        # Стандартна логіка /start без параметрів
        await message.answer("Виникла проблема, повторіть авторизацію")


from cloudinary import uploader, config as cloudinary_config


@router.message(StateFilter(UserProgress.numbers), F.contact)
async def register_city(message: Message, state: FSMContext):
    from main import bot

    await message.answer("Дані зберігаються...", reply_markup=ReplyKeyboardRemove())
    contact = message.contact
    phone_raw = getattr(contact, "phone_number", None)
    await state.update_data(numbers=phone_raw)
    data = await state.get_data()
    number = data.get("numbers")

    # Google Sheets авторизація
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

    print(number)
    print(str(num))

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
        user_data += [0] * 121
        sheet.append_row(user_data)
        await message.answer(
            "Номер підтверджено. Вітаємо в клубі розумників та розумниць! 😉"
        )
        await bot.set_my_commands(
            [BotCommand(command="menu", description="Показати меню")],
            scope=BotCommandScopeChat(chat_id=message.chat.id),
        )
        await message.answer(
            "Привіт! Вітаємо тебе в боті FivOne. Тут зібрані курси та марафони, які створила команда спеціалістів і які допоможуть тобі опанувати нові знання легко, цікаво та весело! Cпостерігати за своїм прогресом ти зможеш в особистому профілі на сайті https://fivone.education/statistics або в боті.",
        )
        await message.answer(
            "Натискай кнопку Меню (на телефоні - три рисочки внизу зліва). Ця кнопка завжди повертатиме тебе до Головного меню. Обирай марафон чи курс, який тебе зацікавив, ознайомлюйся з матеріалами уроку, виконуй завдання та дивуй своїми новими знаннями оточуючих! Запрошуй друзів приєднатися, адже разом дізнаватися щось нове завжди цікавіше! Починаймо! \n👇",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
        await state.update_data(allow=[1])
    else:
        await message.answer(
            "Номер не співпадає з вказаним при авторизації. Автаризуйтеся через номер, на якому зареєстрований телеграм"
        )
        await state.clear()


@router.message(Command("start"))
async def regular_start_handler(message: Message, state: FSMContext):
    from main import bot, redis

    await message.answer(
        "Привіт! Вітаємо тебе в боті FivOne. Тут зібрані курси та марафони, які створила команда спеціалістів і які допоможуть тобі опанувати нові знання легко, цікаво та весело!",
    )

    data = await state.get_data() or {}

    if FREE_ACCESS_MODE:
        # Форсуємо доступ на час недоступності сайту
        await state.update_data(allow=[1])

        # Запам'ятовуємо user_id у Redis — знадобиться, щоб потім
        # розіслати саме цим людям прохання зареєструватись
        await redis.sadd("free_access_users", message.from_user.id)

        if not data.get("notified_free_access"):
            await state.update_data(notified_free_access=True)
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>Зараз йде доробка функції збереження прогресу. Ця функція буде доступна через декілька днів. Коли функція буде додана Вам прийде лист, де потрібно буде зареєструватись на сайті, після чого Ви отримаєте можливість зберігати прогрес!</b>",
                parse_mode="HTML",
            )
    else:
        if "allow" not in data:
            await state.update_data(allow=[0])

    data = await state.get_data()
    allow = data.get("allow", [])
    if allow[0] == 1:
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
    else:
        await message.answer(
            "Щоб отримати доступ до бота, треба зареєструватись на сайті (https://fivone.education/). Після реєстрації ти зможеш спостерігати за своїм прогресом в особистому профілі на сайті або в боті.",
        )

@router.message(F.text == "Про нас")
async def about_us(message: Message, state: FSMContext):
    from main import bot

    await bot.send_message(
        chat_id=message.chat.id,
        text="🎓 <b>Привіт! Ми — команда FivOne!</b>\n\nВсі матеріали створені командою освітнього центру FivOne. Онлайн-школа припинила свою роботу у лютому 2022 року, але більшість розроблених марафонів та курсів ми зберегли тут та залишили в вільному доступі.<b>Команда освітнього центру:</b>\n\n<b>Каріна Семенко</b> - засновниця FivOne та методистка курсів та марафонів.\n<b>Людмила Булигіна</b> - лекторка курсу та марафону з ІТ.\n<b>Едуард Квашин</b> - ментор курсу з ІТ.\n<b>Ярина Мамчур</b> - лекторка курсу з фізики.\n<b>Владислав Дудін</b> - ментор курсу з фізики та автор марафону з фізики.\n<b>Марʼяна Боднар</b> - лекторка курсу та марафону з креативності.\n<b>Ірина Тищенко</b> - лекторка Новорічного марафону.\n\n<b>Розробники боту:</b>\nІлля Рибачик та Вячеслав Рибачик\n\n<b>Приємного навчання!</b> 🙌🤍",
        parse_mode="HTML",
    )


@router.message(F.text == "Прогрес у курсах")
async def progress_curs(message: Message, state: FSMContext):
    from main import bot

    data = await state.get_data()
    statisticC = data.get("statisticC", [])

    alls = 0

    await bot.send_message(
        chat_id=message.chat.id,
        text="<b>Твій прогрес:</b>",
        parse_mode="HTML",
    )

    labels = ["Пройдено", "Залишилось"]
    sumF = statisticC[0][0]
    sizes = [(sumF / 10) * 100, (1 - sumF / 10) * 100]
    colors = ["#04FA0C", "#FF0000"]

    # Створення діаграми
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    # Запис у пам’ять
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    # Обгортання в BufferedInputFile
    photo = BufferedInputFile(buffer.read(), filename="chart.png")

    # Надсилання
    if sumF != 0:
        alls += 1
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f"📊 Твій прогрес у курсі з розвитку креативності: {statisticC[0][0]} / 10",
        )

    sumC = statisticC[1][0]
    sizes = [(sumC / 10) * 100, (1 - sumC / 10) * 100]
    colors = ["#04FA0C", "#FF0000"]

    # Створення діаграми
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    # Запис у пам’ять
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    # Обгортання в BufferedInputFile
    photo = BufferedInputFile(buffer.read(), filename="chart.png")

    # Надсилання
    if sumC != 0:
        alls += 1
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f"📊 Твій прогрес у курсі з фізика навколо нас: {statisticC[1][0]} / 10",
        )

    sumK = statisticC[2][0]
    sizes = [(sumK / 9) * 100, (1 - sumK / 9) * 100]
    colors = ["#04FA0C", "#FF0000"]

    # Створення діаграми
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    # Запис у пам’ять
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    # Обгортання в BufferedInputFile
    photo = BufferedInputFile(buffer.read(), filename="chart.png")

    # Надсилання
    if sumK != 0:
        alls += 1
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f"📊 Твій прогрес у курсі з старт програмування: {statisticC[2][0]} / 9",
        )

    if alls == 0:
        await bot.send_message(
            chat_id=message.chat.id,
            text="<b>Поки що без прогресу</b> 😊\nАле це лише початок — у тебе все ще попереду!\n\nЩоб твій прогрес зарахувався, не забудь натиснути кнопку  \n<b>«Позначити як виконаний»</b> ✅\n\n📌 У <b>курсах</b> — після останньої частини заняття.",
            parse_mode="HTML",
        )
        alls = 0


@router.message(F.text == "Прогрес у марафонах")
async def progress_marafons(message: Message, state: FSMContext):
    from main import bot

    data = await state.get_data()
    statisticM = data.get("statisticM", [])

    alls = 0

    await bot.send_message(
        chat_id=message.chat.id,
        text="<b>Твій прогрес:</b>",
        parse_mode="HTML",
    )

    labels = ["Пройдено", "Залишилось"]
    sumF = statisticM[0][0] + statisticM[0][1] + statisticM[0][2]
    sizes = [(sumF / 20) * 100, (1 - sumF / 20) * 100]
    colors = ["#04FA0C", "#FF0000"]

    # Створення діаграми
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    # Запис у пам’ять
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    # Обгортання в BufferedInputFile
    photo = BufferedInputFile(buffer.read(), filename="chart.png")

    # Надсилання
    if sumF != 0:
        alls += 1
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f"📊 Твій прогрес у марафоні з фізики\n\nТиждень 1: {statisticM[0][0]} / 7\nТиждень 2: {statisticM[0][1]} / 6\nТиждень 3: {statisticM[0][2]} / 7",
        )

    sumC = statisticM[1][0] + statisticM[1][1] + statisticM[1][2]
    sizes = [(sumC / 18) * 100, (1 - sumC / 18) * 100]
    colors = ["#04FA0C", "#FF0000"]

    # Створення діаграми
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    # Запис у пам’ять
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    # Обгортання в BufferedInputFile
    photo = BufferedInputFile(buffer.read(), filename="chart.png")

    # Надсилання
    if sumC != 0:
        alls += 1
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f"📊 Твій прогрес у марафоні з хімії\n\nТиждень 1: {statisticM[1][0]} / 6\nТиждень 2: {statisticM[1][1]} / 6\nТиждень 3: {statisticM[1][2]} / 6",
        )

    sumK = statisticM[2][0] + statisticM[2][1] + statisticM[2][2]
    sizes = [(sumK / 19) * 100, (1 - sumK / 19) * 100]
    colors = ["#04FA0C", "#FF0000"]

    # Створення діаграми
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    # Запис у пам’ять
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    # Обгортання в BufferedInputFile
    photo = BufferedInputFile(buffer.read(), filename="chart.png")

    # Надсилання
    if sumK != 0:
        alls += 1
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f"📊 Твій прогрес у марафоні з креативності\n\nТиждень 1: {statisticM[2][0]} / 7\nТиждень 2: {statisticM[2][1]} / 7\nТиждень 3: {statisticM[2][2]} / 5",
        )

    sumI = statisticM[3][0] + statisticM[3][1] + statisticM[3][2]
    sizes = [(sumI / 18) * 100, (1 - sumI / 18) * 100]
    colors = ["#04FA0C", "#FF0000"]

    # Створення діаграми
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    # Запис у пам’ять
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    # Обгортання в BufferedInputFile
    photo = BufferedInputFile(buffer.read(), filename="chart.png")

    # Надсилання
    if sumI != 0:
        alls += 1
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f"📊 Твій прогрес у марафоні з програмування\n\nТиждень 1: {statisticM[3][0]} / 6\nТиждень 2: {statisticM[3][1]} / 6\nТиждень 3: {statisticM[3][2]} / 6",
        )

    sumF = statisticM[4][0]
    sizes = [(sumF / 7) * 100, (1 - sumF / 7) * 100]
    colors = ["#04FA0C", "#FF0000"]

    # Створення діаграми
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    # Запис у пам’ять
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    # Обгортання в BufferedInputFile
    photo = BufferedInputFile(buffer.read(), filename="chart.png")

    # Надсилання
    if sumF != 0:
        alls += 1
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f"📊 Твій прогрес у новорічному марафоні: {statisticM[4][0]} / 7",
        )

    if alls == 0:
        await bot.send_message(
            chat_id=message.chat.id,
            text="<b>Поки що без прогресу</b> 😊\nАле це лише початок — у тебе все ще попереду!\n\nЩоб твій прогрес зарахувався, не забудь натиснути кнопку  \n<b>«Позначити як виконаний»</b> ✅\n\n📌 У <b>марафонах</b> вона знаходиться після уроку.",
            parse_mode="HTML",
        )
        alls = 0


@router.message(F.text == "Твій прогрес")
async def regular_start_handler(message: Message, state: FSMContext):
    button_text = "Перейти до сайту"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{button_text}",
                    url="https://fivone.education/statistics",
                )
            ]
        ]
    )
    if FREE_ACCESS_MODE:
        await message.answer(
            text="<b>Зараз йде доробка функції збереження прогресу. Ця функція буде доступна через декілька днів. Коли функція буде додана Вам прийде лист, де потрібно буде зареєструватись на сайті, після чого Ви отримаєте можливість зберігати прогрес!</b>",
            parse_mode="HTML",
        )
    else:
        await message.answer(
            "Також спостерігати за своїм прогресом ти зможеш в особистому профілі на сайті https://fivone.education/statistics.",
            reply_markup=keyboard,
        )
    await message.answer(
        "Вибери, де ти хочеш подивитися свій прогрес: у курсах чи марафонах.",
        reply_markup=kb.progress,
    )

def generate_all_button_lists(LESSONS, CURS) -> dict:
    """Генерує всі списки кнопок з JSON"""
    result = {}

    # Курси
    for course_idx in range(len(CURS)):
        course = CURS[course_idx]
        tasks = []
        lesson_num = 1
        for key in sorted(course.keys()):
            if key.startswith("tesks_"):
                text = course[key].get("text", key)
                clean = text.replace("<b>", "").replace("</b>", "")
                tasks.append(f"{clean[:50]}")
                lesson_num += 1
        tasks.append("Повернутися до курсів")
        result[f"task{course_idx}"] = tasks

    # Марафони
    marathon_keys = [
        ("leson", 0, 0), ("lesonForWeekSecond", 0, 1), ("lesonForWeekThird", 0, 2),
        ("leson", 1, 0), ("lesonForWeekSecond", 1, 1), ("lesonForWeekThird", 1, 2),
        ("leson", 2, 0), ("lesonForWeekSecond", 2, 1), ("lesonForWeekThird", 2, 2),
        ("leson", 3, 0), ("lesonForWeekSecond", 3, 1), ("lesonForWeekThird", 3, 2),
        ("leson", 4, 0),
    ]

    key_names = {
        ("leson", 0): "leson0", ("lesonForWeekSecond", 0): "lesonForWeekSecond0",
        ("lesonForWeekThird", 0): "lesonForWeekThird0",
        ("leson", 1): "leson1", ("lesonForWeekSecond", 1): "lesonForWeekSecond1",
        ("lesonForWeekThird", 1): "lesonForWeekThird1",
        ("leson", 2): "leson2", ("lesonForWeekSecond", 2): "lesonForWeekSecond2",
        ("lesonForWeekThird", 2): "lesonForWeekThird2",
        ("leson", 3): "leson3", ("lesonForWeekSecond", 3): "lesonForWeekSecond3",
        ("lesonForWeekThird", 3): "lesonForWeekThird3",
        ("leson", 4): "leson4",
    }

    back_buttons = {
        "leson4": "Повернутися до марафонів",
    }

    for prefix, m_idx, w_idx in marathon_keys:
        if m_idx >= len(LESSONS):
            continue
        week_key = f"week_{w_idx}"
        if week_key not in LESSONS[m_idx]:
            continue
        week = LESSONS[m_idx][week_key]
        lessons_list = []
        lesson_num = 1
        for wkey in sorted(week.keys()):
            if wkey.startswith("tesks_"):
                text = week[wkey].get("text", wkey)
                clean = text.replace("<b>", "").replace("</b>", "")
                lessons_list.append(f"{clean[:50]}")
                lesson_num += 1
        back = back_buttons.get(key_names.get((prefix, m_idx), ""), "Повернутися до тижнів")
        lessons_list.append(back)
        result[key_names.get((prefix, m_idx), f"{prefix}{m_idx}")] = lessons_list

    # Тижні
    result["wek0"] = ["Марафон з фізики. Тиждень 1", "Марафон з фізики. Тиждень 2", "Марафон з фізики. Тиждень 3", "Повернутися до марафонів"]
    result["wek1"] = ["Марафон з хімії. Тиждень 1", "Марафон з хімії. Тиждень 2", "Марафон з хімії. Тиждень 3", "Повернутися до марафонів"]
    result["wek2"] = ["Марафон з креативності. Тиждень 1", "Марафон з креативності. Тиждень 2", "Марафон з креативності. Тиждень 3", "Повернутися до марафонів"]
    result["wek3"] = ["Марафон з IT. Тиждень 1", "Марафон з IT. Тиждень 2", "Марафон з IT. Тиждень 3", "Повернутися до марафонів"]
    result["wek4"] = ["Наворічний марафон. Тиждень 1", "Повернутися до марафонів"]

    result["marafonskey0"] = ["Фізика", "Хімія", "Креативність", "Програмування", "Новорічний", "Повернутися до головного меню"]
    result["Curskey0"] = ["Курс. Розвиток креативності", "Курс. Фізика навколо нас", "Курс. Старт програмування. Мова С++", "Повернутися до головного меню"]

    return result


async def refresh_button_names(state: FSMContext):
    """Оновлює назви кнопок з JSON зберігаючи галочки"""
    from app import storage_json

    data = await state.get_data()
    new_lists = generate_all_button_lists(storage_json.LESSONS, storage_json.CURS)

    updated = {}
    for key, new_list in new_lists.items():
        old_list = data.get(key, [])
        if not old_list:
            updated[key] = new_list
            continue

        merged = []
        for i, new_item in enumerate(new_list):
            if i < len(old_list):
                # Зберігаємо галочку якщо була
                has_check = old_list[i].endswith(" ✅")
                merged.append(f"{new_item} ✅" if has_check else new_item)
            else:
                merged.append(new_item)
        updated[key] = merged

    await state.update_data(**updated)

@router.message(Command("menu"))
async def start(message: Message, state: FSMContext):
    from app import storage_json

    data = await state.get_data() or {}
    allow = data.get("allow", [])

    if allow[0] == 1:
        if "go" in data:
            # Оновлюємо назви з JSON зберігаючи галочки
            await refresh_button_names(state)
        else:
            # Перший вхід — ініціалізуємо все
            await state.update_data(
                statisticM=[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0]],
                statisticC=[[0], [0], [0]],
                ends=0,
                dzM=[],
                indexM=[0],
                indexWeekM=[0, 0],
                go=True,
                kof=[0],
                les=[],
                num=[],
                way=[],
                dzC=[],
                Cursnum=[],
                Cursway=[],
                Cursles=[],
                Curskof=[0],
                Cursends=0,
                indexC=[0],
                explat=[],
                imgCr=[],
                parts_of_tasks=[],
                dzPart=[],
                Exp=[],
                kN=[],
                last_part=0,
                **generate_all_button_lists(storage_json.LESSONS, storage_json.CURS)
            )
        await message.answer("Обирайте марафон чи курс", reply_markup=main)
    else:
        await message.answer(
            "Щоб отримати доступ до бота, треба зареєструватись на сайті (https://fivone.education/).",
        )


@router.message(F.text == "Повернутися до головного меню")
async def start(message: Message):
    await message.answer("Обирайте марафон чи курс", reply_markup=main)


# Marafophons


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
        "<b>Структура марафонів</b>\n\nКожен наш марафон має свою структуру, щоб тобі було зручно навчатись і все було по кроках\n\nЗазвичай марафон триває три тижні - ти поступово проходиш нові теми, отримуєш підтримку й бачиш свій прогрес.\nА от новорічний марафон - особливий 🎄, він триває лише один тиждень, але наповнений святковим настроєм і цікавими завданнями!\n\nНа початку кожного марафону ти отримуєш теоретичну частину - коротке відео з поясненнями та текстовий документ із основними матеріалами.\nПісля цього можеш натиснути кнопку «Отримати домашнє завдання», щоб відкрити свої завдання.\nА коли все зробиш - натисни «Перевірити себе», і система покаже тести, щоб ти міг переконатися, що все зрозумів 💪\n\n✨ Обирай марафон, який тебе зацікавив, - і вперед до нових знань!",
        reply_markup=lessonKeyboard,
        parse_mode="HTML",
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
    if index != 4:
        lessonKeyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=lesson)] for lesson in week],
            resize_keyboard=True,
        )
        await message.answer("Обери тиждень", reply_markup=lessonKeyboard)
    else:
        index = 0
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
                "Перейти на наступний тиждень",
            ]
        )
    )
)
async def LessonMAR(message: Message, state: FSMContext):
    from main import bot

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
        data = await state.get_data()
        indexM = data.get("indexM", [])
        next_or_no_next = 0
        next_w_or_no_next_w = 0
        for i in lessons:
            if i == str(message.text[:6]):
                if i == "Наступ":
                    indexM[0] = int(indexM[0]) + 1
                    next_or_no_next = 1
                    next_w_or_no_next_w = 0
                elif i == "Перейт":
                    indexM[0] = 0
                    next_or_no_next = 1
                    next_w_or_no_next_w = 1
                else:
                    indexM[0] = lessons.index(i)
                    next_or_no_next = 0
                    next_w_or_no_next_w = 0
        # num.append(index)
        data = await state.get_data()
        way = data.get("way", [])
        indexWeekM = data.get("indexWeekM", [])
        if next_w_or_no_next_w == 0:
            await state.update_data(num=[way[0], way[1], indexM[0]])
            indexWeekM[0] = int(way[0])
            indexWeekM[1] = int(way[1]) + 1
        else:
            await state.update_data(num=[indexWeekM[0], indexWeekM[1], indexM[0]])
        await state.update_data(indexWeekM=indexWeekM)
    await state.update_data(les=[])
    # data = await state.get_data()
    # les = data.get("les", [])
    # les.append(way[0])
    # les.append(way[1])
    # les.append(index)
    data = await state.get_data()
    way = data.get("way", [])
    change_reply_murkup_or_not = 0
    if next_w_or_no_next_w == 0:
        await state.update_data(les=[way[0], way[1], indexM[0]])
    else:
        await state.update_data(les=[indexWeekM[0], indexWeekM[1], indexM[0]])
        num = data.get("num", [])

        if num[1] == 0:
            keyboard_name = f"leson{num[0]}"
        elif num[1] == 1:
            keyboard_name = f"lesonForWeekSecond{num[0]}"
        else:
            keyboard_name = f"lesonForWeekThird{num[0]}"

        data = await state.get_data()
        week = data.get(keyboard_name, [])
        lessonKeyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=lesson)] for lesson in week],
            resize_keyboard=True,
        )
        change_reply_murkup_or_not = 1

    await state.update_data(indexM=indexM)
    data = await state.get_data()
    num = data.get("num", [])

    lesson = storage_json.LESSONS[int(num[0])]
    week = lesson[f"week_{int(num[1])}"]
    tesks = week[f"tesks_{int(num[2])}"]
    image = FSInputFile(tesks["image"])
    caption = f"<b>{tesks['text']}</b>"
    if change_reply_murkup_or_not == 0:
        if next_or_no_next == 0:
            await message.answer_photo(photo=image, caption=caption, parse_mode="HTML")
        else:
            await bot.send_photo(
                chat_id=message.chat.id, photo=image, caption=caption, parse_mode="HTML"
            )
    else:
        if next_or_no_next == 0:
            await message.answer_photo(
                photo=image,
                caption=caption,
                parse_mode="HTML",
                reply_markup=lessonKeyboard,
            )
        else:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=image,
                caption=caption,
                parse_mode="HTML",
                reply_markup=lessonKeyboard,
            )
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
        if next_or_no_next == 0:
            await message.answer(
                text,
                reply_markup=keyboard,
                parse_mode="HTML",
                disable_web_page_preview=False,
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML",
                disable_web_page_preview=False,
            )

    document = tesks["docs"]
    caption = tesks["textDocs"]
    text = f'<a href="{document}">{caption}</a>'
    if document != "0":
        if next_or_no_next == 0:
            await message.answer(
                text,
                parse_mode="HTML",
                disable_web_page_preview=False,
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                parse_mode="HTML",
                disable_web_page_preview=False,
            )
    data = await state.get_data()
    dzM = data.get("dzM", [])
    dzM = tesks
    await state.update_data(dzM=dzM)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Отримати домашнє завдання", callback_data="dzMM"
                )
            ]
        ]
    )
    if next_or_no_next == 0:
        await message.answer(
            text="Настав час закріпити знання! Натисни кнопку, щоб отримати домашнє завдання 📚",
            reply_markup=keyboard,
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Настав час закріпити знання! Натисни кнопку, щоб отримати домашнє завдання 📚",
            reply_markup=keyboard,
        )


# Curs


@router.message(F.text.in_(["Курси", "Повернутися до курсів"]))
async def Task(message: Message, state: FSMContext):
    await state.update_data(Cursnum=[])
    await state.update_data(Cursway=[])
    data = await state.get_data()
    curskey = data.get("Curskey0", [])
    lessonKeyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lesson)] for lesson in curskey],
        resize_keyboard=True,
    )
    await message.answer(
        "<b>Структура курсів</b>\n\nКожен наш курс має свою структуру, створену так, щоб навчання було зручним і послідовним 🎓\n\nУ кожному курсі є 10 занять, які поділені на частини.\nТак ти можеш легко обрати саме ту тему або момент, який хочеш переглянути ще раз 💡\n\nПісля перегляду матеріалів натисни кнопку «Отримати домашнє завдання», щоб відкрити практичні завдання - вони допоможуть закріпити нові знання та застосувати їх на практиці 💪\n\n✨ Обирай, будь ласка, курс, який тебе зацікавив!",
        reply_markup=lessonKeyboard,
        parse_mode="HTML",
    )


@router.message(
    F.text.startswith(
        tuple(
            [
                "Курс. Розвиток креативності",
                "Курс. Фізика навколо нас",
                "Курс. Старт програмування. Мова С++",
                "Повернутись до занять",
            ]
        )
    )
)
async def Curses(message: Message, state: FSMContext):
    if "✅" in message.text:
        mes = message.text[:-2]
    else:
        mes = message.text
    for i in Curs:
        if i == str(mes):
            index = Curs.index(i)
    data = await state.get_data()
    Cursway = data.get("Cursway", [])
    Cursway.append(index)
    await state.update_data(Cursway=Cursway)
    if index == 0:
        await message.answer(
            "<b>Привіт-привіт!</b> 😄\nВітаємо тебе на курсі з розвитку креативності.\n\nУ цьому курсі на тебе чекає <b>10 занять</b>.\nКожне заняття поділене на кілька частин із відеолекціями та поясненнями.\nПісля деяких частин ти отримуватимеш <b>домашні завдання</b> для закріплення матеріалу.\n\nПісля проходження <b>останньої частини заняття</b> ти зможеш відмітити, що завершив його.\nІнформація про пройдені заняття буде відображатися у <b>твоїй статистиці</b> 📊\n\nТи можеш переглядати відео та виконувати завдання у будь-який зручний для тебе час.\n\nОтже, <b>3-2-1 — починаємо мислити нестандартно</b> ☀️",
            parse_mode="HTML",
        )
    elif index == 1:
        await message.answer(
            "<b>Привіт-привіт!</b> 😄\nВітаємо тебе на курсі з фізики.\n\nУ цьому курсі на тебе чекає <b>10 занять</b>.\nКожне заняття поділене на кілька частин із відеолекціями та поясненнями.\n<b>Після кожної частини</b> ти отримуватимеш <b>домашнє завдання</b> — експеримент або симуляцію з відповідної теми.\n\nПісля проходження <b>останньої частини заняття</b> ти зможеш відмітити, що завершив його.\nІнформація про пройдені заняття буде відображатися у <b>твоїй статистиці</b> 📊\n\nТи можеш переглядати відеолекції та виконувати завдання у будь-який зручний для тебе час.\n\nОтже, <b>3-2-1 — полеееетіли!</b> 🚀",
            parse_mode="HTML",
        )
    elif index == 2:
        await message.answer(
            "<b>Привіт-привіт!</b> 😄\nВітаємо тебе на курсі з Програмування.\n\nУ цьому курсі на тебе чекає <b>10 занять</b>.\nКожне заняття поділене на кілька частин із відеолекціями.\nПісля <b>деяких частин</b> ти отримуватимеш <b>домашні завдання</b> для закріплення матеріалу.\nА в окремих частинах на тебе чекатимуть <b>відео з практикою</b>, де ти зможеш побачити, як працює код у реальних прикладах.\n\nПісля проходження <b>останньої частини заняття</b> ти зможеш відмітити, що завершив його.\nІнформація про пройдені заняття буде відображатися у <b>твоїй статистиці</b> 📊\n\nТи можеш переглядати відео та виконувати завдання у будь-який зручний для тебе час.\n\nОтже, <b>3-2-1 — Побігли-ии-иии!</b> 💻🔥",
            parse_mode="HTML",
        )
    else:
        pass
    data = await state.get_data()
    Cursway = data.get("Cursway", [])
    if Cursway[0] == 3:
        data = await state.get_data()
        Cursles = data.get("Cursles", [])
        await state.update_data(Cursway=[])
        t = Cursles[0]
        await state.update_data(Cursles=[])
        data = await state.get_data()
        Cursway = data.get("Cursway", [])
        Cursway.append(t)
        await state.update_data(Cursway=Cursway)
    else:
        t = Cursway[0]
        await state.update_data(Cursway=[])
        data = await state.get_data()
        Cursway = data.get("Cursway", [])
        Cursway.append(t)
        await state.update_data(Cursway=Cursway)
    await state.update_data(Curskof=[0])
    data = await state.get_data()
    Cursf = f"task{t}"
    Cursweek = data.get(Cursf, [])
    lessonKeyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lesson)] for lesson in Cursweek],
        resize_keyboard=True,
    )
    await message.answer("Обери заняття", reply_markup=lessonKeyboard)


@router.message(
    F.text.startswith(
        tuple(
            [
                "Заняття 1",
                "Заняття 2",
                "Заняття 3",
                "Заняття 4",
                "Заняття 5",
                "Заняття 6",
                "Заняття 7",
                "Заняття 8",
                "Заняття 9",
                "Заняття 10",
                "Наступне заняття",
            ]
        )
    )
)
async def LessonCurs(message: Message, state: FSMContext):
    from main import bot

    data = await state.get_data()
    Curskof = data.get("Curskof", [])
    Cursles = data.get("Cursles", [])
    Cursway = data.get("Cursway", [])
    if Curskof[0] == 1:
        await state.update_data(Cursway=[])
        data = await state.get_data()
        Cursway = data.get("Cursway", [])
        Cursway.append(Cursles[0])
        # Cursway.append(les[1])
        await state.update_data(Cursway=Cursway)
        data = await state.get_data()
        Cursway = data.get("Cursway", [])
    data = await state.get_data()
    indexC = data.get("indexC", [])
    if len(Cursway) != 0:
        # num.append(way[0])
        # num.append(way[1])
        data = await state.get_data()
        indexC = data.get("indexC", [])
        for i in tasks:
            if i == str(message.text[:10]):
                if i == "Наступне з":
                    indexC[0] = int(indexC[0]) + 1
                    next_or_no_next = 1
                else:
                    indexC[0] = tasks.index(i)
                    next_or_no_next = 0

        # num.append(index)
        data = await state.get_data()
        Cursway = data.get("Cursway", [])
        await state.update_data(Cursnum=[Cursway[0], indexC[0]])
    await state.update_data(Cursles=[])
    data = await state.get_data()
    Cursway = data.get("Cursway", [])
    await state.update_data(Cursles=[Cursway[0], indexC[0]])
    await state.update_data(indexC=indexC)
    data = await state.get_data()
    Cursnum = data.get("Cursnum", [])
    lesson = storage_json.CURS[int(Cursnum[0])]
    tesks = lesson[f"tesks_{int(Cursnum[1])}"]
    t = tesks["text"]

    await bot.send_message(
        chat_id=message.chat.id,
        text=t,
        parse_mode="HTML",
        disable_web_page_preview=False,
    )
    if int(tesks["amount_of_video"]) != 0:
        parts_of_taskss = []
        for i in range(0, int(tesks["amount_of_video"])):
            parts_of_taskss.append(
                f"Частина {i+1}. {textV(int(Cursnum[0]), int(Cursnum[1]), int(i))}"
            )
        parts_of_taskss.append(
            f"Повернутись до занять",
        )
        partKeyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=lesson)] for lesson in parts_of_taskss],
            resize_keyboard=True,
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="Обери частину заняття",
            reply_markup=partKeyboard,
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="На жаль, заняття поки що недоступне.",
        )


@router.message(
    F.text.startswith(
        tuple(
            [
                "Частина 1.",
                "Частина 2.",
                "Частина 3.",
                "Частина 4.",
                "Частина 5.",
                "Частина 6.",
                "Частина 7.",
                "Частина 8.",
                "Частина 9.",
                "Частина 10",
            ]
        )
    )
)
async def LessonpartCurs(message: Message, state: FSMContext):
    from main import bot

    data = await state.get_data()
    Cursnum = data.get("Cursnum", [])
    lesson = storage_json.CURS[int(Cursnum[0])]
    # week = lesson[f"week_{int(num[1])}"]
    tesks = lesson[f"tesks_{int(Cursnum[1])}"]
    data = await state.get_data()
    dzC = data.get("dzC", [])
    dzC = tesks
    await state.update_data(dzC=dzC)
    n = 0
    for i in range(0, int(tesks["amount_of_video"])):
        n += 1
    k = 0
    for i in parts_of_task:
        if i == message.text[:10]:
            if k == (n - 1):
                await state.update_data(last_part=1)
                break
            else:
                break
        else:
            k += 1

    await bot.send_message(
        chat_id=message.chat.id,
        text=f"<b>Частина {k+1}. {tesks[f"textVideo{k}"]}</b>",
        parse_mode="HTML",
    )

    textVideo = tesks[f"textVideo{k}"]
    video_url = tesks[f"video_url{k}"]

    text = f'<a href="{video_url}">{textVideo}\n#відео 👇</a>'
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Дивитись відео. {textVideo}", url=f"{video_url}"
                )
            ]
        ]
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML",
        disable_web_page_preview=False,
    )

    if f"textVideoPractise{k}" in tesks:
        textVideo = tesks[f"textVideoPractise{k}"]
        video_url = tesks[f"video_url_Practise{k}"]
        text = f'<a href="{video_url}">{textVideo}\n#відео. Практика 👇</a>'
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Дивитись відео. {textVideo}", url=f"{video_url}"
                    )
                ]
            ]
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
            disable_web_page_preview=False,
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Отримати домашнє завдання", callback_data="dzCC"
                )
            ]
        ]
    )

    data = await state.get_data()
    Exp = data.get("Exp", [])
    if "explain" in tesks:
        if k == 7:
            Exp = "1"
        else:
            Exp = "0"
    else:
        Exp = "0"

    await state.update_data(Exp=Exp)

    data = await state.get_data()
    dzPart = data.get("dzPart", [])
    if f"task{k}" in tesks:
        dzPart = tesks[f"task{k}"]
        if int(tesks["amount_of_video"]) == k+1:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Настав час закріпити знання! Натисни кнопку, щоб отримати домашнє завдання 📚",
                reply_markup=keyboard,
            )
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=f"Отримати завдання", callback_data="dzCC"
                        )
                    ]
                ]
            )
            await bot.send_message(
                chat_id=message.chat.id,
                text="Натисни кнопку, щоб отримати завдання для самоперевірки 📚",
                reply_markup=keyboard,
            )
    else:
        dzPart = "0"
    await state.update_data(dzPart=dzPart)

    data = await state.get_data()
    kN = k

    await state.update_data(kN=kN)

    if f"task{k}" in tesks:
        pass
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Наступна частина заняття",
                        callback_data="refresh_part_tasks",
                    )
                ]
            ]
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="Готовий до наступної частини заняття? 🚀",
            reply_markup=keyboard,
        )


def textV(i, j, k):
    lesson = storage_json.CURS[i]
    tesks = lesson[f"tesks_{j}"]

    textVideo = tesks[f"textVideo{k}"]
    return textVideo


