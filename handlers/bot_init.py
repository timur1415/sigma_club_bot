import logging
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    PicklePersistence,
)

from config.config import TOKEN

from handlers.common_handler import start

from config.states import MAIN_MENU

from handlers.common_handler import join, why

from handlers.payment_handler import pay

from fastapi import FastAPI, Request


def create_bot_app():
    persistence = PicklePersistence(filepath="club_bot")
    telegram_app = ApplicationBuilder().token(TOKEN).persistence(persistence).build()

    conv_hadler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(join, "join"),
                CallbackQueryHandler(pay, "pay"),
                CallbackQueryHandler(start, "sub"),
                CallbackQueryHandler(why, "why"),
                CallbackQueryHandler(start, "main_menu"),
            ]
        },
        name="club_bot",
        persistent=True,
        fallbacks=[CommandHandler("start", start)],
    )


    telegram_app.add_handler(conv_hadler)

    return telegram_app