from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)
from config.config import Configuration

import uuid

from yookassa import Payment


async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(Configuration.account_id)
    print(Configuration.secret_key)

    payment = Payment.create(
        {
            "amount": {"value": "100.00", "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/sigma_club_bot",
            },
            "capture": True,
            "description": "Заказ №1",
        },
        uuid.uuid4(),
    )
    url = payment.confirmation.confirmation_url

    keyboard = [[InlineKeyboardButton("оплатить", url=url)]]
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="давай деньги",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
