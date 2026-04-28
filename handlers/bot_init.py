import logging
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    PicklePersistence,
    ChatJoinRequestHandler
)

from config.config import TOKEN, DEBUG

from handlers.common_handler import start

from config.states import MAIN_MENU

from handlers.common_handler import join, why

from handlers.payment_handler import pay

from fastapi import FastAPI, Request

from handlers.chat_join import chat_join

from handlers.jobs import chek_sub_status

from datetime import time 

from zoneinfo import ZoneInfo

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


    telegram_app.add_handler(ChatJoinRequestHandler(chat_join))
    telegram_app.add_handler(conv_hadler)
    telegram_app.job_queue.run_once(chek_sub_status, 5)

    if not DEBUG:
        telegram_app.job_queue.run_daily(chek_sub_status, time(12, tzinfo=ZoneInfo("Europe/Moscow")))



    return telegram_app