import json
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.drive_storage import download_json, upload_json
from config import Config
import main as app_main

router = Router()

# ===== ADMIN IDs =====
ADMIN_IDS = [1364672042, 928741410]

# ===== States =====
class AdminStates(StatesGroup):
    choosing_content_type = State()
    choosing_course = State()
    choosing_course_lesson = State()
    choosing_course_field = State()
    choosing_course_part = State()
    editing_course_value = State()
    choosing_marathon = State()
    choosing_marathon_week = State()
    choosing_marathon_lesson = State()
    choosing_marathon_field = State()
    choosing_marathon_test = State()
    choosing_marathon_test_field = State()
    editing_marathon_value = State()

# ===== Helpers =====
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def load_curs() -> list:
    return download_json(Config.CURS_JSON_FILE_ID)

def save_curs(data: list):
    upload_json(Config.CURS_JSON_FILE_ID, data)
    app_main.CURS = data  # ← оновлюємо в пам'яті щоб бот одразу бачив зміни

def load_lessons() -> list:
    return download_json(Config.LESSONS_JSON_FILE_ID)

def save_lessons(data: list):
    upload_json(Config.LESSONS_JSON_FILE_ID, data)
    app_main.LESSONS = data

def make_keyboard(buttons: list, add_back=True) -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text=b)] for b in buttons]
    if add_back:
        kb.append([KeyboardButton(text="🔙 Назад"), KeyboardButton(text="❌ Вийти з адміна")])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_curs_part_fields(tesks: dict, part_idx: int) -> dict:
    fields = {}
    k = part_idx
    if f"textVideo{k}" in tesks:
        fields[f"📌 Назва відео {k+1}"] = f"textVideo{k}"
    if f"video_url{k}" in tesks:
        fields[f"🔗 Посилання на відео {k+1}"] = f"video_url{k}"
    if f"textVideoPractise{k}" in tesks:
        fields[f"📌 Назва практики {k+1}"] = f"textVideoPractise{k}"
    if f"video_url_Practise{k}" in tesks:
        fields[f"🔗 Посилання на практику {k+1}"] = f"video_url_Practise{k}"
    if f"task{k}" in tesks:
        fields[f"📋 Завдання {k+1}"] = f"task{k}"
    return fields

MARATHON_LESSON_FIELDS = {
    "📝 Назва уроку": "text",
    "🔗 Посилання на відео": "video_url",
    "📄 Посилання на документ": "docs",
    "📋 Домашнє завдання": "dz",
    "🔘 Текст кнопки відео": "button_text",
}

MARATHON_TEST_FIELDS = {
    "❓ Питання": "question",
    "✅ Пояснення": "explanation",
}

WEEK_NAMES = ["Тиждень 1", "Тиждень 2", "Тиждень 3"]

# ===== /admin entry =====
@router.message(Command("admin"))
async def admin_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔️ У тебе немає доступу до адмін панелі.")
        return
    await state.set_state(AdminStates.choosing_content_type)
    await message.answer(
        "👋 Вітаю в адмін панелі!\nЩо хочеш редагувати?",
        reply_markup=make_keyboard(["📚 Курси", "🏃 Марафони"], add_back=False)
    )

# ===== Exit =====
@router.message(F.text == "❌ Вийти з адміна", StateFilter("*"))
async def admin_exit(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.answer(
        "Вийшов з адмін панелі.",
        reply_markup=ReplyKeyboardRemove()
    )

# ===== COURSES FLOW =====

@router.message(AdminStates.choosing_content_type, F.text == "📚 Курси")
@router.message(AdminStates.choosing_content_type, F.text == "📚 Перейти до курсів")
@router.message(AdminStates.choosing_content_type, F.text == "📚 Ще раз редагувати курси")
async def admin_choose_course(message: Message, state: FSMContext):
    curs = load_curs()
    names = [c["title"] for c in curs]
    await state.set_state(AdminStates.choosing_course)
    await message.answer("Обери курс:", reply_markup=make_keyboard(names))

@router.message(AdminStates.choosing_course)
async def admin_choose_course_lesson(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await admin_start(message, state)
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    curs = load_curs()
    course_idx = next((i for i, c in enumerate(curs) if c["title"] == message.text), None)
    if course_idx is None:
        await message.answer("Курс не знайдено. Спробуй ще раз.")
        return

    await state.update_data(course_idx=course_idx)
    course = curs[course_idx]

    lessons = []
    for key in course:
        if key.startswith("tesks_"):
            lesson_text = course[key].get("text", key)
            clean = lesson_text.replace("<b>", "").replace("</b>", "")
            lessons.append(clean[:60])

    await state.update_data(course_lessons=lessons)
    await state.set_state(AdminStates.choosing_course_lesson)
    await message.answer("Обери заняття:", reply_markup=make_keyboard(lessons))

@router.message(AdminStates.choosing_course_lesson)
async def admin_course_lesson_handler(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await admin_choose_course(message, state)
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    data = await state.get_data()
    lessons = data.get("course_lessons", [])
    lesson_idx = next((i for i, l in enumerate(lessons) if l == message.text), None)
    if lesson_idx is None:
        await message.answer("Заняття не знайдено.")
        return

    await state.update_data(lesson_idx=lesson_idx)
    curs = load_curs()
    course_idx = data["course_idx"]
    tesks = curs[course_idx][f"tesks_{lesson_idx}"]
    amount = int(tesks.get("amount_of_video", 0))

    options = ["📝 Назва заняття"]
    for i in range(amount):
        options.append(f"🎬 Частина {i+1}")
    options.append("📋 Фінальне завдання (task)")

    await state.update_data(course_amount=amount)
    await state.set_state(AdminStates.choosing_course_field)
    await message.answer("Що редагуємо?", reply_markup=make_keyboard(options))

@router.message(AdminStates.choosing_course_field)
async def admin_course_field_selected(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        data = await state.get_data()
        lessons = data.get("course_lessons", [])
        await state.set_state(AdminStates.choosing_course_lesson)
        await message.answer("Обери заняття:", reply_markup=make_keyboard(lessons))
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    data = await state.get_data()

    if message.text == "📝 Назва заняття":
        await state.update_data(edit_field="text", edit_part=None)
        curs = load_curs()
        current = curs[data["course_idx"]][f"tesks_{data['lesson_idx']}"]["text"]
        await state.set_state(AdminStates.editing_course_value)
        await message.answer(
            f"Поточне значення:\n\n{current}\n\n✏️ Введи нове значення:",
            reply_markup=make_keyboard(["🔙 Назад", "❌ Вийти з адміна"], add_back=False),
            parse_mode="HTML"
        )
        return

    if message.text == "📋 Фінальне завдання (task)":
        await state.update_data(edit_field="task", edit_part=None)
        curs = load_curs()
        current = curs[data["course_idx"]][f"tesks_{data['lesson_idx']}"].get("task", "")
        await state.set_state(AdminStates.editing_course_value)
        await message.answer(
            f"Поточне значення:\n\n{current}\n\n✏️ Введи нове значення:",
            reply_markup=make_keyboard(["🔙 Назад", "❌ Вийти з адміна"], add_back=False),
            parse_mode="HTML"
        )
        return

    if message.text.startswith("🎬 Частина"):
        part_num = int(message.text.split()[-1]) - 1
        await state.update_data(edit_part=part_num)

        curs = load_curs()
        tesks = curs[data["course_idx"]][f"tesks_{data['lesson_idx']}"]
        fields = get_curs_part_fields(tesks, part_num)

        if not fields:
            await message.answer("Немає полів для редагування в цій частині.")
            return

        await state.update_data(part_fields=fields)
        await state.set_state(AdminStates.choosing_course_part)
        await message.answer(
            f"Що редагуємо в Частині {part_num+1}?",
            reply_markup=make_keyboard(list(fields.keys()))
        )

@router.message(AdminStates.choosing_course_part)
async def admin_course_part_field(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        data = await state.get_data()
        amount = int(data.get("course_amount", 0))
        options = ["📝 Назва заняття"]
        for i in range(amount):
            options.append(f"🎬 Частина {i+1}")
        options.append("📋 Фінальне завдання (task)")
        await state.set_state(AdminStates.choosing_course_field)
        await message.answer("Що редагуємо?", reply_markup=make_keyboard(options))
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    data = await state.get_data()
    fields = data.get("part_fields", {})
    field_key = fields.get(message.text)
    if not field_key:
        await message.answer("Поле не знайдено.")
        return

    await state.update_data(edit_field=field_key)
    curs = load_curs()
    current = curs[data["course_idx"]][f"tesks_{data['lesson_idx']}"].get(field_key, "")
    await state.set_state(AdminStates.editing_course_value)
    await message.answer(
        f"Поточне значення:\n\n{current}\n\n✏️ Введи нове значення:",
        reply_markup=make_keyboard(["🔙 Назад", "❌ Вийти з адміна"], add_back=False),
        parse_mode="HTML"
    )

@router.message(AdminStates.editing_course_value)
async def admin_save_course_value(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        data = await state.get_data()
        edit_part = data.get("edit_part")
        if edit_part is not None:
            # Повертаємось до вибору поля частини
            fields = get_curs_part_fields(
                load_curs()[data["course_idx"]][f"tesks_{data['lesson_idx']}"],
                edit_part
            )
            await state.update_data(part_fields=fields)
            await state.set_state(AdminStates.choosing_course_part)
            await message.answer(
                f"Що редагуємо в Частині {edit_part+1}?",
                reply_markup=make_keyboard(list(fields.keys()))
            )
        else:
            # Повертаємось до вибору поля заняття
            amount = int(data.get("course_amount", 0))
            options = ["📝 Назва заняття"]
            for i in range(amount):
                options.append(f"🎬 Частина {i+1}")
            options.append("📋 Фінальне завдання (task)")
            await state.set_state(AdminStates.choosing_course_field)
            await message.answer("Що редагуємо?", reply_markup=make_keyboard(options))
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    data = await state.get_data()
    new_value = message.text
    field = data["edit_field"]

    curs = load_curs()
    curs[data["course_idx"]][f"tesks_{data['lesson_idx']}"][field] = new_value
    save_curs(curs)

    await message.answer(
        f"✅ Збережено!\n\nПоле <b>{field}</b> оновлено.",
        parse_mode="HTML",
        reply_markup=make_keyboard(["📚 Ще раз редагувати курси", "🏃 Перейти до марафонів", "❌ Вийти з адміна"], add_back=False)
    )
    await state.set_state(AdminStates.choosing_content_type)

# ===== MARATHONS FLOW =====

@router.message(AdminStates.choosing_content_type, F.text == "🏃 Марафони")
@router.message(AdminStates.choosing_content_type, F.text == "🏃 Перейти до марафонів")
@router.message(AdminStates.choosing_content_type, F.text == "🏃 Ще раз редагувати марафони")
async def admin_choose_marathon(message: Message, state: FSMContext):
    lessons = load_lessons()
    names = [m["title"] for m in lessons]
    await state.set_state(AdminStates.choosing_marathon)
    await message.answer("Обери марафон:", reply_markup=make_keyboard(names))

@router.message(AdminStates.choosing_marathon)
async def admin_choose_week(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await admin_start(message, state)
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    lessons = load_lessons()
    marathon_idx = next((i for i, m in enumerate(lessons) if m["title"] == message.text), None)
    if marathon_idx is None:
        await message.answer("Марафон не знайдено.")
        return

    await state.update_data(marathon_idx=marathon_idx)
    marathon = lessons[marathon_idx]

    weeks = []
    for i in range(3):
        if f"week_{i}" in marathon:
            weeks.append(f"Тиждень {i+1}")

    if len(weeks) == 1:
        await state.update_data(week_idx=0)
        await state.set_state(AdminStates.choosing_marathon_lesson)
        await show_marathon_lessons(message, state)
        return

    await state.update_data(marathon_weeks=weeks)
    await state.set_state(AdminStates.choosing_marathon_week)
    await message.answer("Обери тиждень:", reply_markup=make_keyboard(weeks))

@router.message(AdminStates.choosing_marathon_week)
async def admin_marathon_week_handler(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        # Повертаємось до вибору марафону
        lessons = load_lessons()
        names = [m["title"] for m in lessons]
        await state.set_state(AdminStates.choosing_marathon)
        await message.answer("Обери марафон:", reply_markup=make_keyboard(names))
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    week_idx = next((i for i, w in enumerate(WEEK_NAMES) if w == message.text), None)
    if week_idx is None:
        await message.answer("Тиждень не знайдено.")
        return

    await state.update_data(week_idx=week_idx)
    await state.set_state(AdminStates.choosing_marathon_lesson)
    await show_marathon_lessons(message, state)

async def show_marathon_lessons(message: Message, state: FSMContext):
    data = await state.get_data()
    lessons = load_lessons()
    marathon = lessons[data["marathon_idx"]]
    week = marathon[f"week_{data['week_idx']}"]

    lesson_names = []
    for key in week:
        if key.startswith("tesks_"):
            lesson_text = week[key].get("text", key)
            clean = lesson_text.replace("<b>", "").replace("</b>", "")
            lesson_names.append(clean[:60])

    await state.update_data(marathon_lessons=lesson_names)
    await message.answer("Обери урок:", reply_markup=make_keyboard(lesson_names))

@router.message(AdminStates.choosing_marathon_lesson)
async def admin_choose_marathon_field(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        data = await state.get_data()
        weeks = data.get("marathon_weeks", [])
        if weeks:
            await state.set_state(AdminStates.choosing_marathon_week)
            await message.answer("Обери тиждень:", reply_markup=make_keyboard(weeks))
        else:
            # Новорічний — одразу назад до марафонів
            lessons = load_lessons()
            names = [m["title"] for m in lessons]
            await state.set_state(AdminStates.choosing_marathon)
            await message.answer("Обери марафон:", reply_markup=make_keyboard(names))
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    data = await state.get_data()
    lessons_list = data.get("marathon_lessons", [])
    lesson_idx = next((i for i, l in enumerate(lessons_list) if l == message.text), None)
    if lesson_idx is None:
        await message.answer("Урок не знайдено.")
        return

    await state.update_data(marathon_lesson_idx=lesson_idx)

    lessons = load_lessons()
    tesks = lessons[data["marathon_idx"]][f"week_{data['week_idx']}"][f"tesks_{lesson_idx}"]
    has_tests = len(tesks.get("test", {})) > 0

    fields = list(MARATHON_LESSON_FIELDS.keys())
    if has_tests:
        fields.append("🧪 Редагувати тести")

    await state.update_data(marathon_fields=fields)
    await state.set_state(AdminStates.choosing_marathon_field)
    await message.answer("Що редагуємо?", reply_markup=make_keyboard(fields))

@router.message(AdminStates.choosing_marathon_field)
async def admin_marathon_field_selected(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        # Повертаємось до вибору уроку
        await state.set_state(AdminStates.choosing_marathon_lesson)
        await show_marathon_lessons(message, state)
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    data = await state.get_data()

    if message.text == "🧪 Редагувати тести":
        lessons = load_lessons()
        tesks = lessons[data["marathon_idx"]][f"week_{data['week_idx']}"][f"tesks_{data['marathon_lesson_idx']}"]
        test_keys = list(tesks["test"].keys())
        test_labels = [f"Тест {i+1}: {tesks['test'][k]['question'][:40]}..." for i, k in enumerate(test_keys)]
        await state.update_data(test_keys=test_keys, test_labels=test_labels)
        await state.set_state(AdminStates.choosing_marathon_test)
        await message.answer("Обери тест:", reply_markup=make_keyboard(test_labels))
        return

    field_key = MARATHON_LESSON_FIELDS.get(message.text)
    if not field_key:
        await message.answer("Поле не знайдено.")
        return

    await state.update_data(edit_field=field_key, edit_context="lesson")
    lessons = load_lessons()
    tesks = lessons[data["marathon_idx"]][f"week_{data['week_idx']}"][f"tesks_{data['marathon_lesson_idx']}"]
    current = tesks.get(field_key, "")

    await state.set_state(AdminStates.editing_marathon_value)
    await message.answer(
        f"Поточне значення:\n\n{current}\n\n✏️ Введи нове значення:",
        reply_markup=make_keyboard(["🔙 Назад", "❌ Вийти з адміна"], add_back=False),
        parse_mode="HTML"
    )

@router.message(AdminStates.choosing_marathon_test)
async def admin_choose_test_field(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        # Повертаємось до вибору поля уроку
        data = await state.get_data()
        fields = data.get("marathon_fields", list(MARATHON_LESSON_FIELDS.keys()))
        await state.set_state(AdminStates.choosing_marathon_field)
        await message.answer("Що редагуємо?", reply_markup=make_keyboard(fields))
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    data = await state.get_data()
    test_labels = data.get("test_labels", [])
    test_idx = next((i for i, l in enumerate(test_labels) if l == message.text), None)
    if test_idx is None:
        await message.answer("Тест не знайдено.")
        return

    await state.update_data(test_idx=test_idx)
    await state.set_state(AdminStates.choosing_marathon_test_field)
    await message.answer(
        "Що редагуємо в тесті?",
        reply_markup=make_keyboard(list(MARATHON_TEST_FIELDS.keys()))
    )

@router.message(AdminStates.choosing_marathon_test_field)
async def admin_marathon_test_field(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        # Повертаємось до вибору тесту
        data = await state.get_data()
        test_labels = data.get("test_labels", [])
        await state.set_state(AdminStates.choosing_marathon_test)
        await message.answer("Обери тест:", reply_markup=make_keyboard(test_labels))
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    field_key = MARATHON_TEST_FIELDS.get(message.text)
    if not field_key:
        await message.answer("Поле не знайдено.")
        return

    await state.update_data(edit_field=field_key, edit_context="test")
    data = await state.get_data()
    lessons = load_lessons()
    test_key = data["test_keys"][data["test_idx"]]
    current = lessons[data["marathon_idx"]][f"week_{data['week_idx']}"][f"tesks_{data['marathon_lesson_idx']}"]["test"][test_key].get(field_key, "")

    await state.set_state(AdminStates.editing_marathon_value)
    await message.answer(
        f"Поточне значення:\n\n{current}\n\n✏️ Введи нове значення:",
        reply_markup=make_keyboard(["🔙 Назад", "❌ Вийти з адміна"], add_back=False),
    )

@router.message(AdminStates.editing_marathon_value)
async def admin_save_marathon_value(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        data = await state.get_data()
        edit_context = data.get("edit_context", "lesson")
        if edit_context == "test":
            # Повертаємось до вибору поля тесту
            await state.set_state(AdminStates.choosing_marathon_test_field)
            await message.answer(
                "Що редагуємо в тесті?",
                reply_markup=make_keyboard(list(MARATHON_TEST_FIELDS.keys()))
            )
        else:
            # Повертаємось до вибору поля уроку
            fields = data.get("marathon_fields", list(MARATHON_LESSON_FIELDS.keys()))
            await state.set_state(AdminStates.choosing_marathon_field)
            await message.answer("Що редагуємо?", reply_markup=make_keyboard(fields))
        return
    if message.text == "❌ Вийти з адміна":
        await admin_exit(message, state)
        return

    data = await state.get_data()
    new_value = message.text
    field = data["edit_field"]
    edit_context = data.get("edit_context", "lesson")

    lessons = load_lessons()
    tesks = lessons[data["marathon_idx"]][f"week_{data['week_idx']}"][f"tesks_{data['marathon_lesson_idx']}"]

    if edit_context == "test":
        test_key = data["test_keys"][data["test_idx"]]
        tesks["test"][test_key][field] = new_value
    else:
        tesks[field] = new_value

    save_lessons(lessons)

    await message.answer(
        f"✅ Збережено!\n\nПоле <b>{field}</b> оновлено.",
        parse_mode="HTML",
        reply_markup=make_keyboard(["🏃 Ще раз редагувати марафони", "📚 Перейти до курсів", "❌ Вийти з адміна"], add_back=False)
    )
    await state.set_state(AdminStates.choosing_content_type)
