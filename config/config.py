import os
from dotenv import load_dotenv
from yookassa import Configuration
load_dotenv()

TGK_ID = os.getenv('TGK')
TOKEN = os.getenv('TOKEN')

Configuration.account_id = 1056362
Configuration.secret_key = os.getenv('YOOKASSA_SECRET')
