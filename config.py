import os
from dotenv import load_dotenv

import os


class Config:
    BOT_TOKEN: str
    ADMIN_ID: int
    DEBUG: bool
    FIRST_DATE: str
    GOOGLE_CREDENTIALS: str
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    @classmethod
    def load(cls):
        load_dotenv()

        cls.GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")
        cls.CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
        cls.CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
        cls.CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
        cls.BOT_TOKEN = os.getenv("BOT_TOKEN")
        if not cls.BOT_TOKEN:
            raise ValueError("❌ BOT_TOKEN is missing!")

        cls.ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
        cls.DEBUG = os.getenv("DEBUG", "False") == "True"
        cls.FIRST_DATE = os.getenv("FIRST_DATE", "")

