from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_number = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Відправити номер телефону", request_contact=True)]],
    resize_keyboard=True,
)

regestration = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Зареєструватись")],
        [KeyboardButton(text="Увійти в акаунт")],
    ],
    resize_keyboard=True,
)

singIn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Увійти в акаунт")],
    ],
    resize_keyboard=True,
)

reg = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Зареєструватись")],
    ],
    resize_keyboard=True,
)

progress = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Прогрес у марафонах")],
        [KeyboardButton(text="Прогрес у курсах")],
        [KeyboardButton(text="Повернутися до головного меню")],
    ],
    resize_keyboard=True,
)
