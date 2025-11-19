import os
from dotenv import load_dotenv
from yookassa import Configuration

load_dotenv()

TGK_ID = os.getenv("TGK")
TOKEN = os.getenv("TOKEN")

Configuration.account_id = 1056362
Configuration.secret_key = os.getenv("YOOKASSA_SECRET")
TELEGRAM_WEBHOOK_PATH = os.getenv("TELEGRAM_WEBHOOK_PATH")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
SECRET_TOKEN = os.getenv("SECRET_TOKEN", '123')
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_ECHO = True if os.getenv("DATABASE_ECHO") == "True" else False