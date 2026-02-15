from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ContextTypes,
    
)

from config.config import WEBHOOK_URL




async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()


    keyboard = [
        [InlineKeyboardButton("1 месяц - 1500р", web_app=WebAppInfo(f'{WEBHOOK_URL}/app'))]
        # [InlineKeyboardButton("3 месяца - 4300р", url=url_3)],
        # [InlineKeyboardButton("6 месяцев - 8500р", url=url_6)],
        # [InlineKeyboardButton("12 месяцев - 16500р", url=url_12)],
    ]

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/rich_hasbik.png", "rb"),
        caption="давай деньги",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    