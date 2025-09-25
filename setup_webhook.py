from telegram import Bot
from config.config import TOKEN

async def register_webhook():   
    bot = Bot(token=TOKEN)
    await bot.set_webhook('https://njfd.ru/telegram/webhook')


