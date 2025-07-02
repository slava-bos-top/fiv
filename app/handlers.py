from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram import Router, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramBadRequest
import json

import app.keyboards as kb

with open("lessons.json", "r", encoding="utf-8") as f:
    LESSONS = json.load(f)

router = Router()

num = []
way = []
marafons = [
    "Фізика",
    "Хімія",
    "Креативність",
    "Програмування",
    "Новорічний",
]
weeks = ["Тиждень 1", "Тиждень 2", "Тиждень 3"]
lessons = ["Урок 1", "Урок 2", "Урок 3", "Урок 4", "Урок 5", "Урок 6", "Урок 7"]

explat = []
imgCr = []


# callback
@router.callback_query(F.data == "Молодець! Так тримати!")
async def homework_done_callback(callback: CallbackQuery):
    await callback.answer("Молодець! Так тримати! ✅", show_alert=True)


@router.callback_query(F.data == "next")
async def homework_done_callbacktask(callback: CallbackQuery):
    keyboard_name = f"lesson{way[0]}"

    selected_keyboard = getattr(kb, keyboard_name)

    await callback.message.answer("Обери урок", reply_markup=selected_keyboard)


@router.callback_query(F.data == "nextsecond")
async def homework_done_callbacktasksec(callback: CallbackQuery):
    keyboard_name = f"lessonForWeekSecond{way[0]}"

    selected_keyboard = getattr(kb, keyboard_name)

    await callback.message.answer("Обери урок", reply_markup=selected_keyboard)


@router.callback_query(F.data == "nextthird")
async def homework_done_callbacktasksec(callback: CallbackQuery):
    keyboard_name = f"lessonForWeekThird{way[0]}"

    selected_keyboard = getattr(kb, keyboard_name)

    await callback.message.answer("Обери урок", reply_markup=selected_keyboard)


@router.callback_query(F.data == "nextweek")
async def homework_done_callbackweek(callback: CallbackQuery):
    await callback.message.answer("Обирай тиждень!", reply_markup=kb.week)


@router.callback_query(F.data == "explation")
async def homework_done_callbacktask(callback: CallbackQuery):
    image = FSInputFile(imgCr[0])
    await callback.message.answer_photo(
        caption=f"{explat[0]}", photo=image, parse_mode="HTML"
    )


# start
@router.message(Command("menu"))
async def start(message: Message):
    await message.answer("Оберайте марафон чи курс", reply_markup=kb.main)


@router.message(F.text == "Марафони")
async def Task(message: Message):
    num.clear()
    way.clear()
    await message.answer("Обери марафон", reply_markup=kb.marafons)


@router.message(
    F.text.in_(
        [
            "Фізика",
            "Хімія",
            "Креативність",
            "Програмування",
            "Новорічний",
        ]
    )
)
async def Marafons(message: Message):
    for i in marafons:
        if i == str(message.text):
            index = marafons.index(i)
    way.append(index)
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
    else:
        image = FSInputFile("app/media/marafons/New/mater.jpg")
        await message.answer_photo(
            photo=image,
            caption="<b>Привіт-привіт! </b>😄\nВітаємо тебе на Новорічному марафоні 🎄\n\nУ цьому каналі протягом тижня ти отримуватимеш відеолекції та завдання від авторів марафону з освітнього центру FivOne. У відео будуть показані всі етапи: від приготування матеріалів до виготовлення іграшок.\n\nТакож у деякі дні тут з'являтимуться додаткові відео, в якому лекторка знайомитиме тебе з матеріалами та даватиме цікаві завдання 😉\n\nТи можеш переглядати відео та майструвати іграшки у будь-який зручний для тебе час.\n\nТакож ось файл з переліком всіх матеріалів (https://drive.google.com/file/d/1SAEblqDHBBaXE5SY68NNLal1vsMprbIa/view?usp=sharing), які тобі знадобляться.\n\n😁 Радимо виготовляти іграшки всією сім'єю або разом з друзями, бо так веселіше!\nДілись з друзями інформацією та запрошуй на марафон!\n\n<b>Це буде класний тиждень! </b>⛄️",
            parse_mode="HTML",
        )
    if index < 4:
        await message.answer("Обери тиждень", reply_markup=kb.week)
    else:
        await message.answer("Обери тиждень", reply_markup=kb.week1)


@router.message(F.text.in_(["Тиждень 1", "Тиждень 2", "Тиждень 3"]))
async def Week(message: Message):
    for i in weeks:
        if i == str(message.text):
            index = weeks.index(i)
    way.append(index)
    if index == 0:
        keyboard_name = f"lesson{way[0]}"

        selected_keyboard = getattr(kb, keyboard_name)

        await message.answer("Обери урок", reply_markup=selected_keyboard)
    elif index == 1:
        keyboard_name = f"lessonForWeekSecond{way[0]}"

        selected_keyboard = getattr(kb, keyboard_name)

        await message.answer("Обери урок", reply_markup=selected_keyboard)
    else:
        keyboard_name = f"lessonForWeekThird{way[0]}"

        selected_keyboard = getattr(kb, keyboard_name)

        await message.answer("Обери урок", reply_markup=selected_keyboard)


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
async def Lesson(message: Message):
    if len(way) != 0:
        num.append(way[0])
        num.append(way[1])
        for i in lessons:
            if i == str(message.text[:6]):
                index = lessons.index(i)
        num.append(index)
    lesson = LESSONS[int(num[0])]
    week = lesson[f"week_{int(num[1])}"]
    tesks = week[f"tesks_{int(num[2])}"]
    image = FSInputFile(tesks["image"])
    caption = f"<b>{tesks['text']}</b>"
    await message.answer_photo(
        photo=image, caption=caption, parse_mode="HTML", reply_markup=kb.main
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
            reply_markup=keyboard,
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
                        reply_markup=keyboard,
                    )
                else:
                    await message.answer(
                        dz,
                        parse_mode="HTML",
                        reply_markup=keyboard,
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
                        reply_markup=keyboard,
                    )
                else:
                    raise e
        else:
            text = f"{dz}"
            await message.answer(
                text,
                disable_web_page_preview=False,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
    else:
        try:
            await message.answer_photo(
                photo=imageexp,
                caption=dz,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        except TelegramBadRequest as e:
            if "caption is too long" in str(e):
                await message.answer(
                    dz,
                    parse_mode="HTML",
                )
                await message.answer_photo(
                    photo=imageexp,
                    reply_markup=keyboard,
                )
            else:
                raise e
    if "docDz" in tesks:
        video = FSInputFile(tesks["docDz"])
        await message.answer_document(
            document=video,
            caption='<b>Зроби додаткове завдання "Таблиця цінностей"</b>',
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    if "docDzn" in tesks:
        await message.answer(
            text=tesks["docDzn"],
            parse_mode="HTML",
            reply_markup=keyboard,
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
                explat.clear()
                imgCr.clear()
                explat.append(test["dop"])
                imgCr.append(test["imgCr"])
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
            reply_markup=keyboard,
        )
    if "addDzn" in tesks:
        text = tesks["addDzn"]
        await message.answer(
            text,
            disable_web_page_preview=False,
            parse_mode="HTML",
            reply_markup=keyboard,
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
        text = f"Відеопояснення до завдання другого тижня на мові С++"
        await message.answer(
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard,
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
    if tesks["End"] == "0":
        num.clear()
        text = "Натисни, щоб обрати інший урок з цього тижня 👇"
        await message.answer(
            text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    elif tesks["End"] == "1":
        num.clear()
        p = way[0]
        way.clear()
        way.append(p)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Обрати інший тиждень", callback_data="nextweek"
                    )
                ]
            ]
        )
        text = "Це був останій урок цього тижня! Продовжуй шлях!"
        await message.answer(text)
        text = "Натисни, щоб обрати інший тиждень 👇"
        await message.answer(
            text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    else:
        text = (
            "Це був останій урок цього марафону! Можеш обрати інший марафон або курс."
        )
        await message.answer(text)
        num.clear()
        way.clear()
