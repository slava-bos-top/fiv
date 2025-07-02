from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Курси")],
        [KeyboardButton(text="Марафони")],
        [KeyboardButton(text="Про нас")],
    ],
    resize_keyboard=True,
)

marafons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Фізика")],
        [KeyboardButton(text="Хімія")],
        [KeyboardButton(text="Креативність")],
        [KeyboardButton(text="Програмування")],
        [KeyboardButton(text="Новорічний")],
    ],
    resize_keyboard=True,
)

week = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Тиждень 1")],
        [KeyboardButton(text="Тиждень 2")],
        [KeyboardButton(text="Тиждень 3")],
    ],
    resize_keyboard=True,
)

week1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Тиждень 1")],
    ],
    resize_keyboard=True,
)

lesson0 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Сила Всесвітнього тяжніння. Невагомість")],
        [KeyboardButton(text="Урок 2. Вільне падіння. Прискорення вільного падіння")],
        [KeyboardButton(text="Урок 3. Центр мас")],
        [KeyboardButton(text="Урок 4. Прості механізми")],
        [KeyboardButton(text="Урок 5. Пружність")],
        [KeyboardButton(text="Урок 6. Тертя")],
        [KeyboardButton(text='Урок 7. Додаткове відео "Чому небо блакитне?"')],
    ],
    resize_keyboard=True,
)

lessonForWeekSecond0 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Температура")],
        [KeyboardButton(text="Урок 2. Енергія")],
        [KeyboardButton(text="Урок 3. Двигуни")],
        [KeyboardButton(text="Урок 4. Густина")],
        [KeyboardButton(text="Урок 5. Тиск")],
        [KeyboardButton(text="Урок 6. Горіння")],
    ],
    resize_keyboard=True,
)

lessonForWeekThird0 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Електрика")],
        [KeyboardButton(text="Урок 2. Лампочка")],
        [KeyboardButton(text="Урок 3. Магніти")],
        [KeyboardButton(text="Урок 4. Оптика")],
        [KeyboardButton(text="Урок 5. Зв'язок")],
        [KeyboardButton(text="Урок 6. Астрофізика")],
    ],
    resize_keyboard=True,
)

lesson1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Явища навколо нас")],
        [KeyboardButton(text="Урок 2. Періодична система Менделєєва")],
        [KeyboardButton(text="Урок 3. Речовини та їхні властивості")],
        [KeyboardButton(text="Урок 4. Атоми, молекули, йони. Маса")],
        [KeyboardButton(text="Урок 5. Речовини (частина 2)")],
        [KeyboardButton(text="Урок 6. Суміші та їхні властивості")],
    ],
    resize_keyboard=True,
)

lessonForWeekSecond1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Суміші (частина 2)")],
        [KeyboardButton(text="Урок 2. Прості та складні речовини")],
        [KeyboardButton(text="Урок 3. Валентність. Формули речовин")],
        [KeyboardButton(text="Урок 4. Закон збереження маси")],
        [KeyboardButton(text="Урок 5. Органічні речовини")],
        [KeyboardButton(text="Урок 6. Експерименти")],
    ],
    resize_keyboard=True,
)

lessonForWeekThird1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Оксиди (Неорганічні речовини)")],
        [KeyboardButton(text="Урок 2. Кислоти (Неорганічні речовини)")],
        [KeyboardButton(text="Урок 3. Основи. Індикатори")],
        [KeyboardButton(text="Урок 4. Солі")],
        [KeyboardButton(text="Урок 5. Чому речовини мають різний колір?")],
        [KeyboardButton(text="Урок 6. Підсумок марафону з хімії")],
    ],
    resize_keyboard=True,
)

lesson2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Що таке креативність?")],
        [KeyboardButton(text="Урок 2. Як шукати нові ідеї?")],
        [KeyboardButton(text="Урок 3. Чому потрібно фантазувати?")],
        [KeyboardButton(text="Урок 4. Чи поєднуються креативність та розум?")],
        [KeyboardButton(text="Урок 5. Які риси мають креативні люди?")],
        [KeyboardButton(text="Урок 6. Фантазійний календар")],
        [KeyboardButton(text="Урок 7. Основи дизайну. Ресурси")],
    ],
    resize_keyboard=True,
)

lessonForWeekSecond2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Що робити, якщо немає ідей?")],
        [KeyboardButton(text="Урок 2. Мистецтво та Творчість")],
        [KeyboardButton(text="Урок 3. Музика та креативність")],
        [KeyboardButton(text="Урок 4. Як театр розвиває креативність?")],
        [KeyboardButton(text="Урок 5. Креативність в інших видах мистецтва")],
        [KeyboardButton(text="Урок 6. Шукаємо натхнення навколо нас")],
        [KeyboardButton(text="Урок 7. Сучасний дизайн. Приклади")],
    ],
    resize_keyboard=True,
)

lessonForWeekThird2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Мрії та візуалізації")],
        [KeyboardButton(text="Урок 2. Цінності та креативність")],
        [KeyboardButton(text="Урок 3. Креативність як частина підприємництва")],
        [KeyboardButton(text="Урок 4. Командна робота у креативній сфері")],
        [KeyboardButton(text="Урок 5. 10 кроків для створення креативних проектів")],
    ],
    resize_keyboard=True,
)

lesson3 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Вступ до програмування")],
        [KeyboardButton(text="Урок 2. Програмування життєвих ситуацій")],
        [KeyboardButton(text="Урок 3. Структура програм")],
        [KeyboardButton(text="Урок 4. Старт програмування. Діалог")],
        [KeyboardButton(text="Урок 5. Додаємо умови в код")],
        [KeyboardButton(text="Урок 6. Мотивація")],
    ],
    resize_keyboard=True,
)

lessonForWeekSecond3 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Основи С++. Арифметика")],
        [KeyboardButton(text="Урок 2. Умови в мові С++")],
        [KeyboardButton(text="Урок 3. Алгоритми у С++")],
        [KeyboardButton(text="Урок 4. Цикли у мові С++")],
        [KeyboardButton(text="Урок 5. Функції. Підключення бібліотек")],
        [KeyboardButton(text="Урок 6. Мотивація")],
    ],
    resize_keyboard=True,
)

lessonForWeekThird3 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Основи мови Python")],
        [KeyboardButton(text="Урок 2. Цикли у мові Python")],
        [KeyboardButton(text="Урок 3. Підключення бібліотек у мові Python")],
        [KeyboardButton(text="Урок 4. Рядки у мові Python")],
        [KeyboardButton(text="Урок 5. Основи JavaScript (підготовка до інтенсиву)")],
        [KeyboardButton(text="Урок 6. Інтенсив JavaScript")],
    ],
    resize_keyboard=True,
)

lesson4 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Урок 1. Іграшка з природних матеріалів")],
        [KeyboardButton(text="Урок 2. Іграшка в техніці канзаши")],
        [KeyboardButton(text="Урок 3. Новорічна іграшка з солоного тіста")],
        [KeyboardButton(text="Урок 4. Іграшка з фетру")],
        [KeyboardButton(text="Урок 5. Квілінг")],
        [KeyboardButton(text="Урок 6. Три іграшки з фоамірану")],
        [KeyboardButton(text="Урок 7. Іграшка у техніці декупаж")],
    ],
    resize_keyboard=True,
)
