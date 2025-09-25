from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)

from datetime import timedelta

from config.config import Configuration

import uuid

from yookassa import Payment

from handlers.jobs import check_payment


async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    print(Configuration.account_id)
    print(Configuration.secret_key)

    payment_1 = Payment.create(
        {
            "amount": {"value": "1500.00", "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/sigma_club_bot",
            },
            "capture": True,
            "description": "подписка на месяц",
        },
        uuid.uuid4(),
    )
    url_1 = payment_1.confirmation.confirmation_url

    payment_3 = Payment.create(
        {
            "amount": {"value": "4300.00", "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/sigma_club_bot",
            },
            "capture": True,
            "description": "подписка на 3 месяца",
        },
        uuid.uuid4(),
    )
    url_3 = payment_3.confirmation.confirmation_url

    payment_6 = Payment.create(
        {
            "amount": {"value": "8500.00", "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/sigma_club_bot",
            },
            "capture": True,
            "description": "подписка на 6 месяцев",
        },
        uuid.uuid4(),
    )
    url_6 = payment_6.confirmation.confirmation_url

    payment_12 = Payment.create(
        {
            "amount": {"value": "16500.00", "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/sigma_club_bot",
            },
            "capture": True,
            "description": "подписка на 12 месяцев",
        },
        uuid.uuid4(),
    )
    url_12 = payment_12.confirmation.confirmation_url

    keyboard = [
        [InlineKeyboardButton("1 месяц - 1500р", url=url_1)],
        [InlineKeyboardButton("3 месяца - 4300р", url=url_3)],
        [InlineKeyboardButton("6 месяцев - 8500р", url=url_6)],
        [InlineKeyboardButton("12 месяцев - 16500р", url=url_12)],
    ]

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/rich_hasbik.png", "rb"),
        caption="давай деньги",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    context.job_queue.run_once(
        check_payment,
        timedelta(seconds=30),
        data={
            "payment_1": payment_1,
            "payment_3": payment_3,
            "payment_6": payment_6,
            "payment_12": payment_12,
        },
        name=f'{update.effective_user.id}_payment',
        user_id=update.effective_user.id       
    )
