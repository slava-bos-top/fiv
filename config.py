import os
from dotenv import load_dotenv

import os


class Config:
    BOT_TOKEN: str
    ADMIN_ID: int
    DEBUG: bool
    FIRST_DATE: str

    @classmethod
    def load(cls):
        load_dotenv()

        cls.BOT_TOKEN = os.getenv("BOT_TOKEN")
        if not cls.BOT_TOKEN:
            raise ValueError("❌ BOT_TOKEN is missing!")

        cls.ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
        cls.DEBUG = os.getenv("DEBUG", "False") == "True"
        cls.FIRST_DATE = os.getenv("FIRST_DATE", "")
