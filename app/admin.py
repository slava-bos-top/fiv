import json
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import Config
 
router = Router()
 
# ===== ADMIN IDs =====
ADMIN_IDS = [769775046, 928741410]  # Додай сюди свої Telegram ID
 
# ===== States =====
class AdminStates(StatesGroup):
    choosing_content_type = State()   # курс або марафон
    # --- Курси ---
    choosing_course = State()
    choosing_course_lesson = State()
    choosing_course_field = State()
    choosing_course_part = State()
    editing_course_value = State()
    # --- Марафони ---
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
 
def load_curs():
    with open("curs.json", "r", encoding="utf-8") as f:
        return json.load(f)
 
def save_curs(data):
    with open("curs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
 
def load_lessons():
    with open("lessons.json", "r", encoding="utf-8") as f:
        return json.load(f)
 
def save_lessons(data):
    with open("lessons.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
 
def make_keyboard(buttons: list, add_back=True) -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text=b)] for b in buttons]
    if add_back:
        kb.append([KeyboardButton(text="🔙 Назад"), KeyboardButton(text="❌ Вийти з адміна")])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
 
# Поля курсу які можна редагувати
CURS_LESSON_FIELDS = {
    "📝 Назва заняття": "text",
}
 
def get_curs_part_fields(tesks: dict, part_idx: int) -> dict:
    """Повертає поля для конкретної частини заняття"""
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
 
# Поля уроку марафону які можна редагувати
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
 
# ===== /admin entry =====
@router.message(Command("admin")) 
async def admin_start(message: Message, state: FSMContext):
    await state.clear() 
    
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
    # ЗАМІСТЬ await state.clear() пишемо це:
    await state.set_state(None) # Це просто скине стан адмінки, але збереже ваші дані в таблиці!
    
    await message.answer(
        "Вийшов з адмін панелі. Тепер ви знову можете користуватися звичайним меню.", 
        reply_markup=ReplyKeyboardRemove() # (Або поверніть сюди вашу звичайну клавіатуру користувача)
    )
 
# ===== COURSES FLOW =====
 
@router.message(AdminStates.choosing_content_type, F.text == "📚 Курси")
async def admin_choose_course(message: Message, state: FSMContext):
    curs = load_curs()
    names = [c["title"] for c in curs]
    await state.set_state(AdminStates.choosing_course)
    await message.answer("Обери курс:", reply_markup=make_keyboard(names))
 
@router.message(AdminStates.choosing_course)
async def admin_choose_course_lesson(message: Message, state: FSMContext):
    if message.text in ["🔙 Назад", "❌ Вийти з адміна"]:
        if message.text == "🔙 Назад":
            await admin_start(message, state)
        else:
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
            # Прибираємо HTML теги для відображення
            clean = lesson_text.replace("<b>", "").replace("</b>", "")
            lessons.append(clean[:60])
 
    await state.update_data(course_lessons=lessons)
    await state.set_state(AdminStates.choosing_course_lesson)
    await message.answer("Обери заняття:", reply_markup=make_keyboard(lessons))
 
@router.message(AdminStates.choosing_course_lesson)
async def admin_choose_course_field(message: Message, state: FSMContext):
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
    tesks_key = f"tesks_{lesson_idx}"
    tesks = curs[course_idx][tesks_key]
    amount = int(tesks.get("amount_of_video", 0))
 
    # Показуємо що редагувати: назву заняття або частини
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
        await state.set_state(AdminStates.choosing_course_lesson)
        await admin_choose_course_lesson.__wrapped__(message, state) if hasattr(admin_choose_course_lesson, '__wrapped__') else None
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
 
    # Якщо обрали частину
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
        await state.set_state(AdminStates.choosing_course_field)
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

@router.message(AdminStates.editing_course_value, F.text == "🔙 Назад")
async def admin_cancel_editing_course(message: Message, state: FSMContext):
    # Повертаємо користувача на крок назад — до вибору того, що редагувати
    await state.set_state(AdminStates.choosing_course_field)
    
    # Знову генеруємо меню вибору полів (копіюємо логіку, яка була в admin_choose_course_lesson)
    data = await state.get_data()
    amount = data.get("course_amount", 0)
    
    options = ["📝 Назва заняття"]
    for i in range(amount):
        options.append(f"🎬 Частина {i+1}")
    options.append("📋 Фінальне завдання (task)")
    
    await message.answer("Редагування скасовано. Що редагуємо?", reply_markup=make_keyboard(options))
 
@router.message(AdminStates.editing_course_value)
async def admin_save_course_value(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await state.set_state(AdminStates.choosing_course_field)
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
 
MARATHON_NAMES = ["Фізика", "Хімія", "Креативність", "Програмування", "Новорічний"]
WEEK_NAMES = ["Тиждень 1", "Тиждень 2", "Тиждень 3"]
 
@router.message(AdminStates.choosing_content_type, F.text == "🏃 Марафони")
async def admin_choose_marathon(message: Message, state: FSMContext):
    lessons = load_lessons()
    names = [m["title"] for m in lessons]
    await state.set_state(AdminStates.choosing_marathon)
    await message.answer("Обери марафон:", reply_markup=make_keyboard(names))
 
@router.message(AdminStates.choosing_content_type, F.text == "📚 Ще раз редагувати курси")
async def admin_again_courses(message: Message, state: FSMContext):
    await admin_choose_course(message, state)
 
@router.message(AdminStates.choosing_content_type, F.text == "🏃 Перейти до марафонів")
async def admin_to_marathons(message: Message, state: FSMContext):
    await admin_choose_marathon(message, state)
 
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
 
    # Визначаємо скільки тижнів
    weeks = []
    for i in range(3):
        if f"week_{i}" in marathon:
            weeks.append(f"Тиждень {i+1}")
 
    if len(weeks) == 1:
        # Новорічний — одразу до уроків
        await state.update_data(week_idx=0)
        await state.set_state(AdminStates.choosing_marathon_lesson)
        await show_marathon_lessons(message, state)
        return
 
    await state.set_state(AdminStates.choosing_marathon_week)
    await message.answer("Обери тиждень:", reply_markup=make_keyboard(weeks))
 
@router.message(AdminStates.choosing_marathon_week)
async def admin_choose_marathon_lesson(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await admin_choose_marathon(message, state)
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
        await state.set_state(AdminStates.choosing_marathon_week)
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
 
    # Перевіряємо чи є тести
    lessons = load_lessons()
    tesks = lessons[data["marathon_idx"]][f"week_{data['week_idx']}"][f"tesks_{lesson_idx}"]
    has_tests = len(tesks.get("test", {})) > 0
 
    fields = list(MARATHON_LESSON_FIELDS.keys())
    if has_tests:
        fields.append("🧪 Редагувати тести")
 
    await state.set_state(AdminStates.choosing_marathon_field)
    await message.answer("Що редагуємо?", reply_markup=make_keyboard(fields))
 
@router.message(AdminStates.choosing_marathon_field)
async def admin_marathon_field_selected(message: Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await state.set_state(AdminStates.choosing_marathon_lesson)
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
 
    await state.update_data(edit_field=field_key)
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
        await state.set_state(AdminStates.choosing_marathon_field)
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
        await state.set_state(AdminStates.choosing_marathon_test)
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
        await state.set_state(AdminStates.choosing_marathon_field)
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
        data.pop("edit_context", None)
 
    save_lessons(lessons)
 
    await message.answer(
        f"✅ Збережено!\n\nПоле <b>{field}</b> оновлено.",
        parse_mode="HTML",
        reply_markup=make_keyboard(["🏃 Ще раз редагувати марафони", "📚 Перейти до курсів", "❌ Вийти з адміна"], add_back=False)
    )
    await state.set_state(AdminStates.choosing_content_type)
 
@router.message(AdminStates.choosing_content_type, F.text == "🏃 Ще раз редагувати марафони")
async def admin_again_marathons(message: Message, state: FSMContext):
    await admin_choose_marathon(message, state)
 
@router.message(AdminStates.choosing_content_type, F.text == "📚 Перейти до курсів")
async def admin_to_courses(message: Message, state: FSMContext):
    await admin_choose_course(message, state)
