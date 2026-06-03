# FivOne Telegram Bot

Телеграм-бот освітнього центру FivOne для проходження курсів та марафонів.

## Технології

- **Python** + **aiogram 3**
- **Redis** — зберігання FSM станів
- **Google Sheets** — база даних користувачів та прогресу
- **Cloudinary** — зберігання аватарок користувачів
- **Railway** — хостинг бота та Redis

---

## Змінні середовища (Railway Variables)

### Сервіс бота

| Змінна | Опис |
|---|---|
| `BOT_TOKEN` | Токен Telegram бота. Отримати у [@BotFather](https://t.me/BotFather) |
| `CLOUDINARY_API_KEY` | API ключ сервісу Cloudinary для завантаження фото |
| `CLOUDINARY_API_SECRET` | Секретний ключ Cloudinary |
| `CLOUDINARY_CLOUD_NAME` | Назва хмари (cloud name) у Cloudinary |
| `DATABASE_URL` | URL бази даних (наразі не використовується активно) |
| `GOOGLE_CREDENTIALS` | JSON рядок з credentials сервісного акаунту Google для доступу до Google Sheets |
| `REDIS_URL` | URL підключення до Redis (формат: `redis://default:password@host:port`) |

### Сервіс Redis

Ці змінні генеруються автоматично Railway при створенні Redis сервісу:

| Змінна | Опис |
|---|---|
| `REDIS_PASSWORD` | Пароль для підключення до Redis |
| `REDIS_PUBLIC_URL` | Публічний URL для підключення до Redis ззовні Railway |
| `REDIS_URL` | Внутрішній URL для підключення до Redis всередині Railway |
| `REDISHOST` | Хост Redis сервера |
| `REDISPASSWORD` | Пароль Redis (дублює `REDIS_PASSWORD`) |
| `REDISPORT` | Порт Redis сервера (зазвичай `6379`) |
| `REDISUSER` | Користувач Redis (зазвичай `default`) |

> **Важливо:** У сервісі бота використовується лише `REDIS_URL`. Решта Redis змінних генеруються автоматично і використовуються для ручного підключення при потребі.

---

## Налаштування Google Credentials

1. Створи сервісний акаунт у [Google Cloud Console](https://console.cloud.google.com/)
2. Надай доступ до Google Sheets та Google Drive
3. Завантаж JSON файл з ключами
4. Вміст файлу стисни в один рядок та встав у змінну `GOOGLE_CREDENTIALS`

```bash
# Приклад перетворення JSON в один рядок
cat cred.json | python -c "import json,sys; print(json.dumps(json.load(sys.stdin)))"
```

5. Надай доступ до таблиці для email сервісного акаунту (вигляд: `name@project.iam.gserviceaccount.com`)

---

## Запуск локально

```bash
# Встановити залежності
pip install -r requirements.txt

# Створити файл .env
cp .env.example .env
# Заповнити змінні у .env

# Запустити бота
python main.py
```

### Приклад `.env` файлу

```env
BOT_TOKEN=your_bot_token
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_CLOUD_NAME=your_cloud_name
DATABASE_URL=your_database_url
GOOGLE_CREDENTIALS={"type":"service_account","project_id":"..."}
REDIS_URL=redis://default:password@localhost:6379
```
